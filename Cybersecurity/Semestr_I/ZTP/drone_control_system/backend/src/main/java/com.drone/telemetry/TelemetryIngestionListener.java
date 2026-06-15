package com.drone.telemetry.service;

import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import com.drone.telemetry.dto.TelemetryMessage;
import com.drone.telemetry.model.TelemetryData;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

/**
 * Subscribes to the telemetry stream and feeds each sample into the
 * {@link TelemetryBatchWriter} for batched persistence (Epic 4.5). This is the
 * persistence-side consumer of the broker; the WebSocket broadcaster and the
 * Redis state cache consume the same channel independently.
 */
@Component
@RequiredArgsConstructor
public class TelemetryIngestionListener {

    private final MessageBroker messageBroker;
    private final TelemetryBatchWriter batchWriter;

    @PostConstruct
    void subscribe() {
        messageBroker.subscribe(BrokerChannels.TELEMETRY, TelemetryMessage.class, this::onTelemetry);
    }

    private void onTelemetry(TelemetryMessage msg) {
        batchWriter.enqueue(TelemetryData.builder()
                .droneId(msg.droneId())
                .timestamp(msg.timestamp())
                .latitude(msg.latitude())
                .longitude(msg.longitude())
                .altitudeMeters(msg.altitudeMeters())
                .speedMetersPerSecond(msg.speedMetersPerSecond())
                .headingDegrees(msg.headingDegrees())
                .batteryPercentage(msg.batteryPercentage())
                .satellites(msg.satellites())
                .flightMode(msg.flightMode())
                .armed(msg.armed())
                .build());
    }
}
