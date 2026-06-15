package com.drone.command.dto;

import com.drone.command.CommandType;
import java.time.Instant;

/**
 * Validated command published to the broker
 * ({@link com.drone.messaging.BrokerChannels#COMMANDS}) for the MAVLink adapter
 * to translate into MAVLink packets. The {@code commandId} correlates the
 * eventual {@link CommandAck} back to the issuing operator.
 */
public record CommandMessage(
        String commandId,
        String clientRequestId,
        String droneId,
        CommandType type,
        Double altitudeMeters,
        Double latitude,
        Double longitude,
        String issuedBy,
        Instant issuedAt
) {
}
