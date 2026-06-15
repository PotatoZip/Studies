package com.drone.mavlink.mock;

import com.drone.mavlink.TelemetryParser;
import com.drone.mavlink.dto.MavlinkPacket;
import com.drone.telemetry.dto.TelemetryMessage;
import java.util.Optional;
import org.springframework.stereotype.Component;

/**
 * Mock {@link TelemetryParser}. Maps the composite telemetry packet emitted by
 * {@link MockMavlinkConnection} into the internal {@link TelemetryMessage},
 * deriving the platform drone id from the MAVLink system id.
 */
@Component
public class MavlinkTelemetryParser implements TelemetryParser {

    /** Drone id convention shared with the command translator: {@code drone-<systemId>}. */
    public static String droneId(int systemId) {
        return "drone-" + systemId;
    }

    @Override
    public Optional<TelemetryMessage> parse(MavlinkPacket packet) {
        if (!MavlinkPacket.COMPOSITE_TELEMETRY.equals(packet.messageType())) {
            return Optional.empty();
        }
        return Optional.of(new TelemetryMessage(
                droneId(packet.systemId()),
                packet.receivedAt(),
                packet.latitude(),
                packet.longitude(),
                packet.relativeAltitudeMeters(),
                packet.groundSpeedMetersPerSecond(),
                packet.headingDegrees(),
                packet.batteryRemainingPercent(),
                packet.satellitesVisible(),
                packet.flightMode(),
                packet.armed()));
    }
}
