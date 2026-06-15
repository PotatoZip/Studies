package com.drone.command;

/**
 * Supported drone commands (Epic 4.3). {@code requiresPosition} /
 * {@code requiresAltitude} drive the validation rules in
 * {@code CommandValidator}.
 */
public enum CommandType {
    /** Arm motors. */
    ARM(false, false),
    /** Disarm motors. */
    DISARM(false, false),
    /** Take off to a target altitude. */
    TAKEOFF(false, true),
    /** Land at the current position. */
    LAND(false, false),
    /** Return to launch. */
    RTL(false, false),
    /** Fly to a waypoint (lat/lon + altitude). */
    GOTO_WAYPOINT(true, true);

    private final boolean requiresPosition;
    private final boolean requiresAltitude;

    CommandType(boolean requiresPosition, boolean requiresAltitude) {
        this.requiresPosition = requiresPosition;
        this.requiresAltitude = requiresAltitude;
    }

    public boolean requiresPosition() {
        return requiresPosition;
    }

    public boolean requiresAltitude() {
        return requiresAltitude;
    }
}
