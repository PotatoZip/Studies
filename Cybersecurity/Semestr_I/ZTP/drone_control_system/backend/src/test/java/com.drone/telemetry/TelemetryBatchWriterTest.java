package com.drone.telemetry;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.timeout;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.drone.telemetry.model.TelemetryData;
import com.drone.telemetry.repository.TelemetryRepository;
import com.drone.telemetry.service.TelemetryBatchWriter;
import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class TelemetryBatchWriterTest {

    @Mock private TelemetryRepository repository;

    private TelemetryBatchWriter writer;

    @BeforeEach
    void setUp() {
        writer = new TelemetryBatchWriter(repository, 3); // small batch for testing
    }

    private TelemetryData sample(String droneId) {
        return TelemetryData.builder()
                .droneId(droneId)
                .timestamp(Instant.now())
                .latitude(51.5)
                .longitude(-0.12)
                .build();
    }

    @Test
    void flushesAutomaticallyWhenBatchSizeReached() {
        writer.enqueue(sample("drone-1"));
        writer.enqueue(sample("drone-1"));
        verify(repository, never()).saveAll(anyList()); // below threshold

        writer.enqueue(sample("drone-1")); // hits size 3 -> async auto flush

        // Flush happens on a dedicated executor (off the ingestion thread), so wait for it.
        ArgumentCaptor<List<TelemetryData>> captor = ArgumentCaptor.forClass(List.class);
        verify(repository, timeout(2000).times(1)).saveAll(captor.capture());
        assertThat(captor.getValue()).hasSize(3);
    }

    @Test
    void scheduledFlushPersistsBufferedSamples() {
        writer.enqueue(sample("drone-1"));
        writer.enqueue(sample("drone-2"));

        writer.scheduledFlush();

        ArgumentCaptor<List<TelemetryData>> captor = ArgumentCaptor.forClass(List.class);
        verify(repository).saveAll(captor.capture());
        assertThat(captor.getValue()).hasSize(2);
    }

    @Test
    void flushOnEmptyBufferDoesNothing() {
        writer.scheduledFlush();
        verify(repository, never()).saveAll(anyList());
    }

    @Test
    void bufferIsClearedAfterFlush() {
        writer.enqueue(sample("drone-1"));
        writer.flush();
        writer.flush(); // nothing left to persist

        verify(repository, times(1)).saveAll(anyList());
    }
}
