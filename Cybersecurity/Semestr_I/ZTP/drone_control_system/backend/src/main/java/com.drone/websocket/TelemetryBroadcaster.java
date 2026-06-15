package com.drone.websocket;

import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import com.drone.telemetry.dto.TelemetryMessage;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;

/**
 * Pushes live telemetry to connected WebSocket clients (Epic 4.1). Subscribes
 * to the broker's telemetry stream and fans each sample out to two STOMP
 * destinations: a per-drone topic for focused views and an all-drones topic for
 * the fleet dashboard.
 */
@Component
@RequiredArgsConstructor
public class TelemetryBroadcaster {

    private final MessageBroker messageBroker;
    private final SimpMessagingTemplate messagingTemplate;

    @PostConstruct
    void subscribe() {
        messageBroker.subscribe(BrokerChannels.TELEMETRY, TelemetryMessage.class, this::broadcast);
    }

    private void broadcast(TelemetryMessage telemetry) {
        messagingTemplate.convertAndSend("/topic/telemetry/" + telemetry.droneId(), telemetry);
        messagingTemplate.convertAndSend("/topic/telemetry", telemetry);
    }
}
