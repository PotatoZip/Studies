package com.drone.command;

import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.drone.command.dto.CommandRequest;
import com.drone.common.exception.InvalidCommandException;
import org.junit.jupiter.api.Test;

class CommandValidatorTest {

    private final CommandValidator validator = new CommandValidator();

    private CommandRequest request(CommandType type, Double alt, Double lat, Double lon) {
        CommandRequest r = new CommandRequest();
        r.setDroneId("drone-1");
        r.setType(type);
        r.setAltitudeMeters(alt);
        r.setLatitude(lat);
        r.setLongitude(lon);
        return r;
    }

    @Test
    void landAndRtlNeedNoParameters() {
        assertThatCode(() -> validator.validate(request(CommandType.LAND, null, null, null)))
                .doesNotThrowAnyException();
        assertThatCode(() -> validator.validate(request(CommandType.RTL, null, null, null)))
                .doesNotThrowAnyException();
    }

    @Test
    void takeoffRequiresAltitude() {
        assertThatThrownBy(() -> validator.validate(request(CommandType.TAKEOFF, null, null, null)))
                .isInstanceOf(InvalidCommandException.class)
                .hasMessageContaining("altitudeMeters");
    }

    @Test
    void takeoffRejectsOutOfRangeAltitude() {
        assertThatThrownBy(() -> validator.validate(request(CommandType.TAKEOFF, 600.0, null, null)))
                .isInstanceOf(InvalidCommandException.class);
        assertThatThrownBy(() -> validator.validate(request(CommandType.TAKEOFF, 0.0, null, null)))
                .isInstanceOf(InvalidCommandException.class);
    }

    @Test
    void takeoffAcceptsValidAltitude() {
        assertThatCode(() -> validator.validate(request(CommandType.TAKEOFF, 50.0, null, null)))
                .doesNotThrowAnyException();
    }

    @Test
    void waypointRequiresCoordinates() {
        assertThatThrownBy(() -> validator.validate(
                request(CommandType.GOTO_WAYPOINT, 30.0, null, null)))
                .isInstanceOf(InvalidCommandException.class)
                .hasMessageContaining("latitude");
    }

    @Test
    void waypointRejectsOutOfRangeCoordinates() {
        assertThatThrownBy(() -> validator.validate(
                request(CommandType.GOTO_WAYPOINT, 30.0, 91.0, 0.0)))
                .isInstanceOf(InvalidCommandException.class);
        assertThatThrownBy(() -> validator.validate(
                request(CommandType.GOTO_WAYPOINT, 30.0, 0.0, 200.0)))
                .isInstanceOf(InvalidCommandException.class);
    }

    @Test
    void waypointAcceptsValidPayload() {
        assertThatCode(() -> validator.validate(
                request(CommandType.GOTO_WAYPOINT, 30.0, 51.5, -0.12)))
                .doesNotThrowAnyException();
    }
}
