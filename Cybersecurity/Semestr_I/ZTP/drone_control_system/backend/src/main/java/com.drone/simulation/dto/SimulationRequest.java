package com.drone.simulation.dto;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Positive;
import lombok.Data;

/**
 * Parameters for a full-pipeline mission simulation. All fields are optional;
 * {@code MissionSimulationService} applies sensible defaults so an empty body
 * runs a standard profile. When a value <em>is</em> supplied it is validated at
 * the boundary (via {@code @Valid} on the controller) so bad input is rejected
 * with 400 rather than silently coerced. Bean Validation skips {@code null}
 * fields, so defaults still apply for omitted values.
 */
@Data
public class SimulationRequest {

    /**
     * Target drone id. Should follow the {@code drone-<number>} convention so the
     * MAVLink system-id mapping stays consistent; pick a number outside the live
     * mock fleet (1..N) to avoid disturbing it. Defaults to {@code drone-901}.
     */
    @Pattern(regexp = "^[A-Za-z0-9_-]{1,64}$",
            message = "droneId must be 1-64 chars of letters, digits, '-' or '_'")
    private String droneId;

    /** Telemetry emission rate in Hz (1-50, default 10). */
    @Min(value = 1, message = "rateHz must be at least 1")
    @Max(value = 50, message = "rateHz must be at most 50")
    private Integer rateHz;

    /** Seconds spent in each major flight phase (1-120, default 4). */
    @Min(value = 1, message = "phaseSeconds must be at least 1")
    @Max(value = 120, message = "phaseSeconds must be at most 120")
    private Integer phaseSeconds;

    @Positive(message = "takeoffAltitudeMeters must be positive")
    @DecimalMax(value = "500.0", message = "takeoffAltitudeMeters must be <= 500")
    private Double takeoffAltitudeMeters; // default 50

    @Positive(message = "cruiseAltitudeMeters must be positive")
    @DecimalMax(value = "500.0", message = "cruiseAltitudeMeters must be <= 500")
    private Double cruiseAltitudeMeters;  // default 80

    @DecimalMin(value = "-90.0") @DecimalMax(value = "90.0")
    private Double homeLatitude;   // default 51.5074
    @DecimalMin(value = "-180.0") @DecimalMax(value = "180.0")
    private Double homeLongitude;  // default -0.1278
    @DecimalMin(value = "-90.0") @DecimalMax(value = "90.0")
    private Double waypointLatitude;   // default home + 0.01
    @DecimalMin(value = "-180.0") @DecimalMax(value = "180.0")
    private Double waypointLongitude;  // default home + 0.01
}
