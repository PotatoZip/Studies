package com.drone.mavlink;

import static org.assertj.core.api.Assertions.assertThat;

import com.drone.command.CommandType;
import com.drone.command.dto.CommandMessage;
import com.drone.mavlink.dto.MavlinkCommandPacket;
import com.drone.mavlink.mock.MavlinkCommandTranslator;
import java.time.Instant;
import org.junit.jupiter.api.Test;

class MavlinkCommandTranslatorTest {

    private final MavlinkCommandTranslator translator = new MavlinkCommandTranslator();

    private CommandMessage command(CommandType type, Double alt, Double lat, Double lon) {
        return new CommandMessage("cmd-1", "req-1", "drone-2", type, alt, lat, lon,
                "operator1", Instant.now());
    }

    @Test
    void takeoffMapsToNavTakeoffWithAltitudeInParam7() {
        MavlinkCommandPacket packet = translator.translate(
                command(CommandType.TAKEOFF, 50.0, null, null));

        assertThat(packet.command()).isEqualTo(MavlinkCommandPacket.MAV_CMD_NAV_TAKEOFF);
        assertThat(packet.targetSystem()).isEqualTo(2);
        assertThat(packet.param7()).isEqualTo(50.0);
        assertThat(packet.correlationId()).isEqualTo("cmd-1");
    }

    @Test
    void waypointMapsLatLonToParam5And6() {
        MavlinkCommandPacket packet = translator.translate(
                command(CommandType.GOTO_WAYPOINT, 30.0, 51.5, -0.12));

        assertThat(packet.command()).isEqualTo(MavlinkCommandPacket.MAV_CMD_NAV_WAYPOINT);
        assertThat(packet.param5()).isEqualTo(51.5);
        assertThat(packet.param6()).isEqualTo(-0.12);
        assertThat(packet.param7()).isEqualTo(30.0);
    }

    @Test
    void armSetsParam1To1AndDisarmTo0() {
        assertThat(translator.translate(command(CommandType.ARM, null, null, null)).param1())
                .isEqualTo(1.0);
        assertThat(translator.translate(command(CommandType.DISARM, null, null, null)).param1())
                .isEqualTo(0.0);
    }

    @Test
    void landAndRtlMapToTheirNavCommands() {
        assertThat(translator.translate(command(CommandType.LAND, null, null, null)).command())
                .isEqualTo(MavlinkCommandPacket.MAV_CMD_NAV_LAND);
        assertThat(translator.translate(command(CommandType.RTL, null, null, null)).command())
                .isEqualTo(MavlinkCommandPacket.MAV_CMD_NAV_RETURN_TO_LAUNCH);
    }

    @Test
    void nullParametersDefaultToZero() {
        MavlinkCommandPacket packet = translator.translate(
                command(CommandType.LAND, null, null, null));
        assertThat(packet.param5()).isZero();
        assertThat(packet.param7()).isZero();
    }

    @Test
    void systemIdParsedFromDroneIdSuffix() {
        assertThat(MavlinkCommandTranslator.systemIdFromDroneId("drone-7")).isEqualTo(7);
        assertThat(MavlinkCommandTranslator.systemIdFromDroneId("malformed")).isEqualTo(1);
        assertThat(MavlinkCommandTranslator.systemIdFromDroneId(null)).isEqualTo(1);
    }
}
