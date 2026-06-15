package com.drone.command;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import com.drone.command.dto.CommandMessage;
import com.drone.command.dto.CommandRequest;
import com.drone.command.dto.CommandResponse;
import com.drone.common.exception.InvalidCommandException;
import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class CommandServiceTest {

    @Mock private CommandValidator validator;
    @Mock private MessageBroker messageBroker;

    private CommandQueueService queue;
    private CommandService commandService;

    @BeforeEach
    void setUp() {
        queue = new CommandQueueService();
        commandService = new CommandService(validator, queue, messageBroker);
    }

    private CommandRequest takeoff() {
        CommandRequest r = new CommandRequest();
        r.setDroneId("drone-1");
        r.setType(CommandType.TAKEOFF);
        r.setAltitudeMeters(50.0);
        return r;
    }

    @Test
    void submitValidatesQueuesAndPublishes() {
        CommandResponse response = commandService.submit(takeoff(), "operator1");

        verify(validator).validate(any(CommandRequest.class));

        ArgumentCaptor<Object> payload = ArgumentCaptor.forClass(Object.class);
        verify(messageBroker).publish(eq(BrokerChannels.COMMANDS), payload.capture());

        CommandMessage published = (CommandMessage) payload.getValue();
        assertThat(published.droneId()).isEqualTo("drone-1");
        assertThat(published.type()).isEqualTo(CommandType.TAKEOFF);
        assertThat(published.altitudeMeters()).isEqualTo(50.0);
        assertThat(published.issuedBy()).isEqualTo("operator1");
        assertThat(published.commandId()).isEqualTo(response.getCommandId());

        // Response reflects dispatch, and the command is tracked + marked SENT.
        assertThat(response.getStatus()).isEqualTo(CommandStatus.SENT);
        assertThat(queue.find(response.getCommandId())).isPresent();
        assertThat(queue.find(response.getCommandId()).get().getStatus())
                .isEqualTo(CommandStatus.SENT);
    }

    @Test
    void submitDoesNotPublishWhenValidationFails() {
        doThrow(new InvalidCommandException("bad")).when(validator).validate(any());

        assertThatThrownBy(() -> commandService.submit(takeoff(), "operator1"))
                .isInstanceOf(InvalidCommandException.class);

        verify(messageBroker, never()).publish(any(), any());
    }
}
