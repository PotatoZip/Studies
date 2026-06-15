package com.drone.websocket;

import com.drone.command.CommandQueueService;
import com.drone.command.CommandStatus;
import com.drone.command.dto.CommandAck;
import com.drone.command.dto.CommandAckNotification;
import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;

/**
 * Routes command acknowledgements back to the specific operator who issued the
 * command (Epic 4.4). Subscribes to the broker's ack stream, resolves the
 * pending command to update its status and find the issuing user, then delivers
 * the ack to that user's private queue ({@code /user/queue/acks}).
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class CommandAckBroadcaster {

    private final MessageBroker messageBroker;
    private final SimpMessagingTemplate messagingTemplate;
    private final CommandQueueService queueService;

    @PostConstruct
    void subscribe() {
        messageBroker.subscribe(BrokerChannels.ACKS, CommandAck.class, this::route);
    }

    private void route(CommandAck ack) {
        CommandStatus status = ack.accepted() ? CommandStatus.ACKNOWLEDGED : CommandStatus.REJECTED;
        queueService.resolve(ack.commandId(), status).ifPresentOrElse(
                pending -> {
                    // Enrich the broker ack with the client correlation id + resolved
                    // status so the operator's UI can match it to the exact submit call.
                    CommandAckNotification notification = new CommandAckNotification(
                            ack.commandId(),
                            pending.getClientRequestId(),
                            pending.getDroneId(),
                            pending.getType(),
                            status,
                            ack.accepted(),
                            ack.detail(),
                            ack.timestamp());
                    messagingTemplate.convertAndSendToUser(
                            pending.getIssuedBy(), "/queue/acks", notification);
                },
                () -> log.warn("Ack for unknown command {}", ack.commandId()));
    }
}
