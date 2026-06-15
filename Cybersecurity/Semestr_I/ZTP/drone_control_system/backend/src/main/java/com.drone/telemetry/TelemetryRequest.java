package com.drone.telemetry.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class TelemetryRequest {

    @NotBlank(message = "Drone ID cannot be blank")
    private String droneId;

    @NotNull(message = "Latitude is required")
    @Min(-90)
    @Max(90)
    private Double latitude;

    @NotNull(message = "Longitude is required")
    @Min(-180)
    @Max(180)
    private Double longitude;

    private Double altitude;
    private Double speed;

    @Min(0)
    @Max(100)
    private Double battery;
}
