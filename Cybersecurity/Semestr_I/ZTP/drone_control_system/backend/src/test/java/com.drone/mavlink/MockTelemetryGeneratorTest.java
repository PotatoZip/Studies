package com.drone.mavlink;

import static org.assertj.core.api.Assertions.assertThat;

import com.drone.mavlink.dto.MavlinkCommandPacket;
import com.drone.mavlink.dto.MavlinkPacket;
import com.drone.mavlink.mock.MockTelemetryGenerator;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MockTelemetryGeneratorTest {

    private MockTelemetryGenerator generator;

    @BeforeEach
    void setUp() {
        generator = new MockTelemetryGenerator(3);
    }

    private MavlinkPacket packetFor(int systemId, List<MavlinkPacket> packets) {
        return packets.stream().filter(p -> p.systemId() == systemId).findFirst().orElseThrow();
    }

    @Test
    void tickEmitsOnePacketPerDrone() {
        List<MavlinkPacket> packets = generator.tick();

        assertThat(packets).hasSize(3);
        assertThat(packets).allMatch(p ->
                p.messageType().equals(MavlinkPacket.COMPOSITE_TELEMETRY));
        assertThat(packets).extracting(MavlinkPacket::systemId)
                .containsExactlyInAnyOrder(1, 2, 3);
    }

    @Test
    void dronesStartDisarmedOnTheGround() {
        MavlinkPacket drone1 = packetFor(1, generator.tick());

        assertThat(drone1.armed()).isFalse();
        assertThat(drone1.relativeAltitudeMeters()).isZero();
    }

    @Test
    void takeoffCommandArmsDroneAndStartsClimb() {
        generator.applyCommand(new MavlinkCommandPacket(
                "c1", 1, MavlinkCommandPacket.MAV_CMD_NAV_TAKEOFF,
                0, 0, 0, 0, 0, 0, 40));

        // Advance the simulation a few steps.
        MavlinkPacket drone1 = null;
        for (int i = 0; i < 5; i++) {
            drone1 = packetFor(1, generator.tick());
        }

        assertThat(drone1.armed()).isTrue();
        assertThat(drone1.flightMode()).isEqualTo("TAKEOFF");
        assertThat(drone1.relativeAltitudeMeters()).isGreaterThan(0.0);
    }

    @Test
    void armThenDisarmTogglesState() {
        generator.applyCommand(new MavlinkCommandPacket(
                "c1", 2, MavlinkCommandPacket.MAV_CMD_COMPONENT_ARM_DISARM,
                1, 0, 0, 0, 0, 0, 0));
        assertThat(packetFor(2, generator.tick()).armed()).isTrue();

        generator.applyCommand(new MavlinkCommandPacket(
                "c2", 2, MavlinkCommandPacket.MAV_CMD_COMPONENT_ARM_DISARM,
                0, 0, 0, 0, 0, 0, 0));
        assertThat(packetFor(2, generator.tick()).armed()).isFalse();
    }

    @Test
    void commandToUnknownSystemIsIgnored() {
        // System 99 does not exist in a 3-drone fleet; must not throw.
        generator.applyCommand(new MavlinkCommandPacket(
                "c1", 99, MavlinkCommandPacket.MAV_CMD_NAV_TAKEOFF,
                0, 0, 0, 0, 0, 0, 40));

        assertThat(generator.tick()).hasSize(3);
    }
}
