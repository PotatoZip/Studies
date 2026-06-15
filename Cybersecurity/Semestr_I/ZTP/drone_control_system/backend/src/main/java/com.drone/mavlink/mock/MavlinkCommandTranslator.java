package com.drone.mavlink.mock;

import com.drone.command.dto.CommandMessage;
import com.drone.mavlink.CommandTranslator;
import com.drone.mavlink.dto.MavlinkCommandPacket;
import org.springframework.stereotype.Component;

/**
 * Mock {@link CommandTranslator}. Maps platform command types onto MAV_CMD
 * codes and packs their parameters into {@code COMMAND_LONG} param slots the
 * way PX4/ArduPilot expect (e.g. takeoff altitude in param7, waypoint lat/lon
 * in param5/param6).
 */
@Component
public class MavlinkCommandTranslator implements CommandTranslator {

    @Override
    public MavlinkCommandPacket translate(CommandMessage cmd) {
        int targetSystem = systemIdFromDroneId(cmd.droneId());
        double alt = cmd.altitudeMeters() != null ? cmd.altitudeMeters() : 0.0;
        double lat = cmd.latitude() != null ? cmd.latitude() : 0.0;
        double lon = cmd.longitude() != null ? cmd.longitude() : 0.0;

        return switch (cmd.type()) {
            case TAKEOFF -> command(cmd, targetSystem,
                    MavlinkCommandPacket.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, alt);
            case LAND -> command(cmd, targetSystem,
                    MavlinkCommandPacket.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0);
            case RTL -> command(cmd, targetSystem,
                    MavlinkCommandPacket.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0);
            case GOTO_WAYPOINT -> command(cmd, targetSystem,
                    MavlinkCommandPacket.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, lat, lon, alt);
            case ARM -> command(cmd, targetSystem,
                    MavlinkCommandPacket.MAV_CMD_COMPONENT_ARM_DISARM, 1, 0, 0, 0, 0, 0, 0);
            case DISARM -> command(cmd, targetSystem,
                    MavlinkCommandPacket.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0);
        };
    }

    private MavlinkCommandPacket command(CommandMessage cmd, int targetSystem, int mavCmd,
                                         double p1, double p2, double p3, double p4,
                                         double p5, double p6, double p7) {
        return new MavlinkCommandPacket(cmd.commandId(), targetSystem, mavCmd,
                p1, p2, p3, p4, p5, p6, p7);
    }

    /** Inverse of {@code MavlinkTelemetryParser.droneId}: {@code drone-<n>} -> n. */
    public static int systemIdFromDroneId(String droneId) {
        if (droneId != null) {
            int dash = droneId.lastIndexOf('-');
            if (dash >= 0 && dash < droneId.length() - 1) {
                try {
                    return Integer.parseInt(droneId.substring(dash + 1));
                } catch (NumberFormatException ignored) {
                    // fall through to default
                }
            }
        }
        return 1;
    }
}
