package com.drone.command.dto;

import com.drone.command.CommandType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

/**
 * REST payload for issuing a drone command. Type-specific requirements
 * (position for waypoints, altitude for takeoff) are enforced by
 * {@code CommandValidator}.
 */
@Data
public class CommandRequest {

    @NotBlank(message = "droneId is required")
    private String droneId;

    @NotNull(message = "command type is required")
    private CommandType type;

    /**
     * Optional client-generated correlation id. Echoed back on the
     * acknowledgement so the frontend can match an ACK to the exact submit call
     * even if the synchronous REST response was lost. Generated server-side when
     * omitted.
     */
    private String clientRequestId;

    /** Target altitude in metres (TAKEOFF, GOTO_WAYPOINT). */
    private Double altitudeMeters;

    /** Target latitude (GOTO_WAYPOINT). */
    private Double latitude;

    /** Target longitude (GOTO_WAYPOINT). */
    private Double longitude;
}
