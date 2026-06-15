package com.drone.command.dto;

import com.drone.command.CommandStatus;
import com.drone.command.CommandType;
import java.time.Instant;

/**
 * Acknowledgement delivered to the operator's private WebSocket queue
 * ({@code /user/queue/acks}). Unlike the raw broker {@link CommandAck}, this
 * carries the {@code clientRequestId} and resolved {@link CommandStatus} so the
 * frontend can correlate the ack with the exact command it submitted.
 */
public record CommandAckNotification(
        String commandId,
        String clientRequestId,
        String droneId,
        CommandType type,
        CommandStatus status,
        boolean accepted,
        String detail,
        Instant timestamp
) {
}
