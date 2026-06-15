package com.drone.command;

import java.time.Instant;
import lombok.Getter;
import lombok.Setter;

/**
 * In-memory record of a command awaiting acknowledgement, tracked by
 * {@link CommandQueueService}. Retains the issuing operator so the eventual ack
 * can be routed back to the right WebSocket session.
 */
@Getter
public class PendingCommand {

    private final String commandId;
    private final String clientRequestId;
    private final String droneId;
    private final CommandType type;
    private final String issuedBy;
    private final Instant queuedAt;

    @Setter
    private volatile CommandStatus status;

    public PendingCommand(String commandId, String clientRequestId, String droneId,
                          CommandType type, String issuedBy) {
        this.commandId = commandId;
        this.clientRequestId = clientRequestId;
        this.droneId = droneId;
        this.type = type;
        this.issuedBy = issuedBy;
        this.queuedAt = Instant.now();
        this.status = CommandStatus.QUEUED;
    }
}
