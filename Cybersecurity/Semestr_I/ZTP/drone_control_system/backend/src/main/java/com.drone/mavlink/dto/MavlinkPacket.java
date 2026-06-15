package com.drone.mavlink.dto;

import java.time.Instant;

/**
 * Simplified inbound MAVLink packet (Epic 3.2). A real adapter would aggregate
 * several MAVLink messages (HEARTBEAT, GLOBAL_POSITION_INT, SYS_STATUS, GPS_RAW)
 * to populate these fields; for the mock we carry a single composite packet
 * whose {@code systemId} is the MAVLink system id of the originating drone.
 */
public record MavlinkPacket(
        int systemId,
        String messageType,
        Instant receivedAt,
        double latitude,
        double longitude,
        double relativeAltitudeMeters,
        double groundSpeedMetersPerSecond,
        double headingDegrees,
        double batteryRemainingPercent,
        int satellitesVisible,
        String flightMode,
        boolean armed
) {
    public static final String COMPOSITE_TELEMETRY = "TELEMETRY_COMPOSITE";
}
