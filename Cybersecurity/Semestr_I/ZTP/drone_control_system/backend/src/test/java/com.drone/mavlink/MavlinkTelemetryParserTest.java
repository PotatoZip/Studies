package com.drone.mavlink;

import static org.assertj.core.api.Assertions.assertThat;

import com.drone.mavlink.dto.MavlinkPacket;
import com.drone.mavlink.mock.MavlinkTelemetryParser;
import com.drone.telemetry.dto.TelemetryMessage;
import java.time.Instant;
import java.util.Optional;
import org.junit.jupiter.api.Test;

class MavlinkTelemetryParserTest {

    private final MavlinkTelemetryParser parser = new MavlinkTelemetryParser();

    private MavlinkPacket packet(String type) {
        return new MavlinkPacket(2, type, Instant.parse("2026-06-01T00:00:00Z"),
                51.5, -0.12, 100.0, 5.0, 90.0, 80.0, 11, "AUTO", true);
    }

    @Test
    void parsesCompositeTelemetryIntoMessage() {
        Optional<TelemetryMessage> result =
                parser.parse(packet(MavlinkPacket.COMPOSITE_TELEMETRY));

        assertThat(result).isPresent();
        TelemetryMessage msg = result.get();
        assertThat(msg.droneId()).isEqualTo("drone-2");
        assertThat(msg.latitude()).isEqualTo(51.5);
        assertThat(msg.altitudeMeters()).isEqualTo(100.0);
        assertThat(msg.satellites()).isEqualTo(11);
        assertThat(msg.flightMode()).isEqualTo("AUTO");
        assertThat(msg.armed()).isTrue();
    }

    @Test
    void ignoresNonTelemetryPacketTypes() {
        assertThat(parser.parse(packet("HEARTBEAT"))).isEmpty();
    }

    @Test
    void droneIdHelperMatchesSystemIdConvention() {
        assertThat(MavlinkTelemetryParser.droneId(5)).isEqualTo("drone-5");
    }
}
