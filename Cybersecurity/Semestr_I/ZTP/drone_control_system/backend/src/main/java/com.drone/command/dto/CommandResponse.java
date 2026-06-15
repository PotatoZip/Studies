package com.drone.command.dto;

import com.drone.command.CommandStatus;
import com.drone.command.CommandType;
import java.time.Instant;
import lombok.Builder;
import lombok.Data;

/**
 * Synchronous REST response returned when a command is accepted by the router.
 * The final outcome arrives asynchronously as a {@link CommandAck} over the
 * operator's WebSocket queue.
 */
@Data
@Builder
public class CommandResponse {
    private String commandId;
    private String clientRequestId;
    private String droneId;
    private CommandType type;
    private CommandStatus status;
    private Instant acceptedAt;
}
