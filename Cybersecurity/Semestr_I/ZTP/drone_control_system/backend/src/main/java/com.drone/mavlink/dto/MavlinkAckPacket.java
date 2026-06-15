package com.drone.mavlink.dto;

/**
 * Inbound command acknowledgement modelled on the MAVLink {@code COMMAND_ACK}
 * message (Epic 3.5). {@code result} follows MAV_RESULT semantics: 0 == ACCEPTED.
 */
public record MavlinkAckPacket(
        String correlationId,
        int systemId,
        int command,
        int result,
        String resultText
) {
    public static final int MAV_RESULT_ACCEPTED = 0;

    public boolean accepted() {
        return result == MAV_RESULT_ACCEPTED;
    }
}
