package com.drone.telemetry.service;

import com.drone.telemetry.model.TelemetryData;
import com.drone.telemetry.repository.TelemetryRepository;
import jakarta.annotation.PreDestroy;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/**
 * Buffers incoming telemetry and writes it to PostgreSQL in batches (Epic 4.5),
 * smoothing the high-frequency telemetry stream into far fewer, larger inserts.
 *
 * <p>{@link #enqueue} is called from the broker listener thread that also feeds
 * the live WebSocket stream, so it must never block: it does a non-blocking
 * {@code offer} and, when the buffer is full, hands the flush off to a dedicated
 * single-thread executor. The DB {@code saveAll} therefore happens off the
 * real-time path. A periodic {@link #scheduledFlush()} drains the tail during
 * quiet periods. {@link #flush()} is guarded by an {@link AtomicBoolean} so
 * overlapping triggers collapse into one writer.
 */
@Slf4j
@Component
public class TelemetryBatchWriter {

    private final TelemetryRepository repository;
    private final int maxBatchSize;
    private final BlockingQueue<TelemetryData> buffer = new LinkedBlockingQueue<>();
    private final AtomicBoolean flushing = new AtomicBoolean(false);
    private final ExecutorService flushExecutor =
            Executors.newSingleThreadExecutor(r -> {
                Thread t = new Thread(r, "telemetry-flush");
                t.setDaemon(true);
                return t;
            });

    public TelemetryBatchWriter(TelemetryRepository repository,
                                @Value("${app.telemetry.batch.max-size:200}") int maxBatchSize) {
        this.repository = repository;
        this.maxBatchSize = maxBatchSize;
    }

    /**
     * Add a sample to the buffer; when full, trigger an asynchronous flush so the
     * caller (real-time ingestion thread) is never blocked on DB I/O.
     */
    public void enqueue(TelemetryData sample) {
        buffer.offer(sample);
        if (buffer.size() >= maxBatchSize) {
            flushExecutor.submit(this::flush);
        }
    }

    /** Periodic safety-net flush for low-traffic periods (runs on the scheduler thread). */
    @Scheduled(fixedDelayString = "${app.telemetry.batch.flush-interval-ms:2000}")
    public void scheduledFlush() {
        flush();
    }

    /** Persist any buffered samples and stop the flush executor on shutdown. */
    @PreDestroy
    void shutdown() {
        flushExecutor.shutdown();
        try {
            if (!flushExecutor.awaitTermination(5, TimeUnit.SECONDS)) {
                flushExecutor.shutdownNow();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        flush(); // drain whatever remains
    }

    /** Drain the buffer and persist it as a single batch. */
    public void flush() {
        // Only one flush at a time; skip if another is already in progress.
        if (!flushing.compareAndSet(false, true)) {
            return;
        }
        try {
            List<TelemetryData> batch = new ArrayList<>(buffer.size());
            buffer.drainTo(batch);
            if (batch.isEmpty()) {
                return;
            }
            repository.saveAll(batch);
            log.debug("Persisted telemetry batch of {} samples", batch.size());
        } catch (Exception e) {
            log.error("Failed to persist telemetry batch: {}", e.getMessage());
        } finally {
            flushing.set(false);
        }
    }
}
