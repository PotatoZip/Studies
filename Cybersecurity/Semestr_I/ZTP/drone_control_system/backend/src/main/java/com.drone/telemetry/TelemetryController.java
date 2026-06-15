package com.drone.telemetry.controller;

import com.drone.telemetry.dto.TelemetryRequest;
import com.drone.telemetry.dto.TelemetryResponse;
import com.drone.telemetry.service.TelemetryService;
import jakarta.validation.Valid;
import java.time.Instant;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Telemetry ingestion and historical retrieval (Epics 4.5 / 4.6).
 *
 * <p>
 * The primary ingestion path is the message broker; {@code /ingest} remains
 * available for direct HTTP posting (testing, non-MAVLink sources). History
 * endpoints back the mission-playback UI. CORS is handled centrally in
 * {@code SecurityConfig}.
 */
@RestController
@RequestMapping("/api/v1/telemetry")
@RequiredArgsConstructor
public class TelemetryController {

    private final TelemetryService telemetryService;

    @PostMapping("/ingest")
    public ResponseEntity<Void> ingestData(@Valid @RequestBody TelemetryRequest request) {
        telemetryService.processIncomingTelemetry(request);
        return new ResponseEntity<>(HttpStatus.CREATED);
    }

    /** Most recent samples (newest first), capped at 100. */
    @GetMapping("/{droneId}/recent")
    public ResponseEntity<List<TelemetryResponse>> getRecentData(@PathVariable String droneId) {
        return ResponseEntity.ok(telemetryService.getRecentTelemetry(droneId));
    }

    /**
     * Paginated historical telemetry within a time window, ascending — for
     * mission playback. {@code from}/{@code to} are ISO-8601 instants; when
     * omitted they default to the last 24 hours.
     */
    @GetMapping("/{droneId}/history")
    public Page<TelemetryResponse> getHistory(
            @PathVariable String droneId,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) Instant from,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) Instant to,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "500") int size) {
        Instant effectiveTo = to != null ? to : Instant.now();
        Instant effectiveFrom = from != null ? from : effectiveTo.minusSeconds(86_400);
        return telemetryService.getHistory(droneId, effectiveFrom, effectiveTo,
                PageRequest.of(page, Math.min(size, 5000)));
    }
}
