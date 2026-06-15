package com.drone.telemetry.service;

import com.drone.telemetry.dto.TelemetryRequest;
import com.drone.telemetry.dto.TelemetryResponse;
import java.time.Instant;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface TelemetryService {

    void processIncomingTelemetry(TelemetryRequest request);

    List<TelemetryResponse> getRecentTelemetry(String droneId);

    /**
     * Paginated historical telemetry within a time window, for mission playback
     * (Epic 4.6).
     */
    Page<TelemetryResponse> getHistory(String droneId, Instant from, Instant to, Pageable pageable);
}
