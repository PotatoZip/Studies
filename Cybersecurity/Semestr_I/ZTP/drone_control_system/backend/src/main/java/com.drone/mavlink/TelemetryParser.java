package com.drone.mavlink;

import com.drone.mavlink.dto.MavlinkPacket;
import com.drone.telemetry.dto.TelemetryMessage;
import java.util.Optional;

/**
 * Telemetry parser (Epic 3.2): translates raw MAVLink packets into the internal
 * {@link TelemetryMessage} DTO. Returns empty for packet types that do not carry
 * telemetry of interest.
 */
public interface TelemetryParser {

    Optional<TelemetryMessage> parse(MavlinkPacket packet);
}
