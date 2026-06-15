package com.drone.telemetry.dto;

import java.time.Instant;

/**
 * Canonical, transport-neutral telemetry sample that flows over the message
 * broker ({@link com.drone.messaging.BrokerChannels#TELEMETRY}).
 *
 * <p>The MAVLink adapter parses raw packets into this shape and publishes it;
 * the WebSocket broadcaster, the Redis latest-state cache and the persistence
 * buffer each consume it independently. Kept as an immutable record so it is
 * safe to share across the broker's listener threads.
 */
public record TelemetryMessage(
        String droneId,
        Instant timestamp,
        double latitude,
        double longitude,
        double altitudeMeters,
        double speedMetersPerSecond,
        double headingDegrees,
        double batteryPercentage,
        int satellites,
        String flightMode,
        boolean armed
) {
}
