package com.drone.command;

import com.drone.command.dto.CommandMessage;
import com.drone.command.dto.CommandRequest;
import com.drone.command.dto.CommandResponse;
import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import java.time.Instant;
import java.util.UUID;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * Command router core (Epic 4.3): validate → queue → forward to the broker.
 * The actual execution happens in the MAVLink adapter; this service returns as
 * soon as the command is accepted and dispatched, with the outcome delivered
 * later via {@link com.drone.command.dto.CommandAck}.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class CommandService {

    private final CommandValidator validator;
    private final CommandQueueService queue;
    private final MessageBroker messageBroker;

    public CommandResponse submit(CommandRequest request, String issuedBy) {
        validator.validate(request);

        String commandId = UUID.randomUUID().toString();
        // Honour a client-supplied correlation id; generate one when absent.
        String clientRequestId = (request.getClientRequestId() != null
                && !request.getClientRequestId().isBlank())
                ? request.getClientRequestId()
                : UUID.randomUUID().toString();

        PendingCommand pending = new PendingCommand(
                commandId, clientRequestId, request.getDroneId(), request.getType(), issuedBy);
        queue.enqueue(pending);

        CommandMessage message = new CommandMessage(
                commandId,
                clientRequestId,
                request.getDroneId(),
                request.getType(),
                request.getAltitudeMeters(),
                request.getLatitude(),
                request.getLongitude(),
                issuedBy,
                Instant.now());

        messageBroker.publish(BrokerChannels.COMMANDS, message);
        queue.updateStatus(commandId, CommandStatus.SENT);
        log.info("Dispatched {} command {} (req={}) to drone {} (by {})",
                request.getType(), commandId, clientRequestId, request.getDroneId(), issuedBy);

        return CommandResponse.builder()
                .commandId(commandId)
                .clientRequestId(clientRequestId)
                .droneId(request.getDroneId())
                .type(request.getType())
                .status(CommandStatus.SENT)
                .acceptedAt(pending.getQueuedAt())
                .build();
    }
}
