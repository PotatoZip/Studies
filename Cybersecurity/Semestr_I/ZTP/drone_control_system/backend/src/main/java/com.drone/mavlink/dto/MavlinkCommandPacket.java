package com.drone.mavlink.dto;

/**
 * Outbound command packet modelled on the MAVLink {@code COMMAND_LONG} message
 * (Epic 3.4). {@code command} is a MAV_CMD code and {@code param1..param7}
 * carry command-specific arguments, mirroring the real protocol.
 */
public record MavlinkCommandPacket(
        String correlationId,
        int targetSystem,
        int command,
        double param1,
        double param2,
        double param3,
        double param4,
        double param5,
        double param6,
        double param7
) {
    // A representative subset of MAV_CMD codes.
    public static final int MAV_CMD_NAV_TAKEOFF = 22;
    public static final int MAV_CMD_NAV_LAND = 21;
    public static final int MAV_CMD_NAV_RETURN_TO_LAUNCH = 20;
    public static final int MAV_CMD_NAV_WAYPOINT = 16;
    public static final int MAV_CMD_COMPONENT_ARM_DISARM = 400;
}
