package com.drone.mavlink;

import com.drone.command.dto.CommandAck;
import com.drone.command.dto.CommandMessage;
import com.drone.mavlink.dto.MavlinkAckPacket;
import com.drone.mavlink.mock.MavlinkTelemetryParser;
import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import jakarta.annotation.PostConstruct;
import java.time.Instant;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * Bridges the MAVLink connection layer to the GCS message broker (Epic 3.3–3.5).
 *
 * <ul>
 *   <li>inbound telemetry packets → parsed → published on the TELEMETRY channel;</li>
 *   <li>commands on the COMMANDS channel → translated → sent over the connection;</li>
 *   <li>inbound command acks → published on the ACKS channel for routing back to
 *       the originating operator.</li>
 * </ul>
 *
 * This is the seam where a real PX4/ArduPilot integration would replace the
 * mock connection without affecting the rest of the backend.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class MavlinkAdapterService {

    private final MavlinkConnection connection;
    private final TelemetryParser telemetryParser;
    private final CommandTranslator commandTranslator;
    private final MessageBroker messageBroker;

    @PostConstruct
    void start() {
        // Inbound telemetry -> broker (Epic 3.3)
        connection.onPacket(packet -> telemetryParser.parse(packet)
                .ifPresent(telemetry -> messageBroker.publish(BrokerChannels.TELEMETRY, telemetry)));

        // Inbound command acks -> broker (Epic 3.5)
        connection.onAck(this::publishAck);

        // Commands from the router -> translate -> connection (Epic 3.4)
        messageBroker.subscribe(BrokerChannels.COMMANDS, CommandMessage.class, this::onCommand);

        connection.connect();
        log.info("MAVLink adapter started");
    }

    private void onCommand(CommandMessage command) {
        connection.send(commandTranslator.translate(command));
    }

    private void publishAck(MavlinkAckPacket ack) {
        CommandAck commandAck = new CommandAck(
                ack.correlationId(),
                MavlinkTelemetryParser.droneId(ack.systemId()),
                ack.accepted(),
                ack.resultText(),
                Instant.now());
        messageBroker.publish(BrokerChannels.ACKS, commandAck);
    }
}
