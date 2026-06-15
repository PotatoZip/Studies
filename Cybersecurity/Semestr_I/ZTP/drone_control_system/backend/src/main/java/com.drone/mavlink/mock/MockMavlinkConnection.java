package com.drone.mavlink.mock;

import com.drone.mavlink.MavlinkConnection;
import com.drone.mavlink.dto.MavlinkAckPacket;
import com.drone.mavlink.dto.MavlinkCommandPacket;
import com.drone.mavlink.dto.MavlinkPacket;
import java.util.function.Consumer;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/**
 * Mock {@link MavlinkConnection} (Epic 3, mocked). Stands in for a real UDP/TCP
 * link to a flight controller: instead of reading the wire, it drives a
 * {@link MockTelemetryGenerator} on a fixed schedule and feeds the generated
 * packets to the registered handler. Sending a command mutates the simulation
 * and immediately emits an accepting {@code COMMAND_ACK}.
 */
@Slf4j
@Component
public class MockMavlinkConnection implements MavlinkConnection {

    private final MockTelemetryGenerator generator;
    private final boolean simulationEnabled;

    private volatile Consumer<MavlinkPacket> packetHandler = p -> { };
    private volatile Consumer<MavlinkAckPacket> ackHandler = a -> { };
    private volatile boolean connected = false;

    public MockMavlinkConnection(MockTelemetryGenerator generator,
                                 @Value("${app.mavlink.simulation.enabled:true}") boolean enabled) {
        this.generator = generator;
        this.simulationEnabled = enabled;
    }

    @Override
    public void connect() {
        connected = true;
        log.info("MockMavlinkConnection connected (simulation {})",
                simulationEnabled ? "enabled" : "disabled");
    }

    @Override
    public void disconnect() {
        connected = false;
        log.info("MockMavlinkConnection disconnected");
    }

    @Override
    public boolean isConnected() {
        return connected;
    }

    @Override
    public void onPacket(Consumer<MavlinkPacket> handler) {
        this.packetHandler = handler;
    }

    @Override
    public void onAck(Consumer<MavlinkAckPacket> handler) {
        this.ackHandler = handler;
    }

    @Override
    public void send(MavlinkCommandPacket packet) {
        log.debug("MAVLink TX -> system {} MAV_CMD {}", packet.targetSystem(), packet.command());
        generator.applyCommand(packet);
        // A real flight controller replies asynchronously with COMMAND_ACK.
        ackHandler.accept(new MavlinkAckPacket(
                packet.correlationId(),
                packet.targetSystem(),
                packet.command(),
                MavlinkAckPacket.MAV_RESULT_ACCEPTED,
                "ACCEPTED"));
    }

    /** Pump simulated telemetry to the registered handler at the configured rate. */
    @Scheduled(fixedDelayString = "${app.mavlink.simulation.interval-ms:1000}")
    void pumpTelemetry() {
        if (!simulationEnabled || !connected) {
            return;
        }
        for (MavlinkPacket packet : generator.tick()) {
            packetHandler.accept(packet);
        }
    }
}
