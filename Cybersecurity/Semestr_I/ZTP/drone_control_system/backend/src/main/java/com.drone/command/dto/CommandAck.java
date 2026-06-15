package com.drone.command.dto;

import java.time.Instant;

/**
 * Acknowledgement emitted by the MAVLink adapter
 * ({@link com.drone.messaging.BrokerChannels#ACKS}) after attempting a command.
 * Routed back to the originating operator over their private WebSocket queue.
 */
public record CommandAck(
        String commandId,
        String droneId,
        boolean accepted,
        String detail,
        Instant timestamp
) {
}
