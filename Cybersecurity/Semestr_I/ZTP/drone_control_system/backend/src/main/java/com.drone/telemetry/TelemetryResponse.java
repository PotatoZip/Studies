package com.drone.telemetry.dto;

import java.time.Instant;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class TelemetryResponse {
    private String droneId;
    private Instant recordedAt;
    private Double latitude;
    private Double longitude;
    private Double altitude;
    private Double speed;
    private Double battery;
}
