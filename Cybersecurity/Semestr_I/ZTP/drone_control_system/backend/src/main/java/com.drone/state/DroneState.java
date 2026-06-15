package com.drone.state;

import com.drone.telemetry.dto.TelemetryMessage;
import java.time.Instant;

/**
 * The "Latest State" snapshot held in Redis for a single drone (Epic 4.2).
 * Existence of the key implies the drone is online; the key's TTL causes stale
 * drones to disappear automatically when telemetry stops arriving.
 */
public record DroneState(
        String droneId,
        Instant lastUpdated,
        TelemetryMessage latest
) {
    public static DroneState from(TelemetryMessage telemetry) {
        return new DroneState(telemetry.droneId(), Instant.now(), telemetry);
    }
}
