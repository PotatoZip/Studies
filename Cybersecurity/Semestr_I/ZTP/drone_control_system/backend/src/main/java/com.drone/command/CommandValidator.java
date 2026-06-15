package com.drone.command;

import com.drone.command.dto.CommandRequest;
import com.drone.common.exception.InvalidCommandException;
import org.springframework.stereotype.Component;

/**
 * Validation layer that runs before a command is forwarded to the broker
 * (Epic 4.3). Bean Validation on {@link CommandRequest} covers presence of
 * droneId/type; this enforces the type-specific semantic rules.
 */
@Component
public class CommandValidator {

    public void validate(CommandRequest request) {
        CommandType type = request.getType();

        if (type.requiresAltitude()) {
            Double alt = request.getAltitudeMeters();
            if (alt == null) {
                throw new InvalidCommandException(type + " requires altitudeMeters");
            }
            if (alt <= 0 || alt > 500) {
                throw new InvalidCommandException("altitudeMeters must be between 0 and 500");
            }
        }

        if (type.requiresPosition()) {
            Double lat = request.getLatitude();
            Double lon = request.getLongitude();
            if (lat == null || lon == null) {
                throw new InvalidCommandException(type + " requires latitude and longitude");
            }
            if (lat < -90 || lat > 90) {
                throw new InvalidCommandException("latitude must be between -90 and 90");
            }
            if (lon < -180 || lon > 180) {
                throw new InvalidCommandException("longitude must be between -180 and 180");
            }
        }
    }
}
