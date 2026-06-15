package com.drone.telemetry.model;

import jakarta.persistence.*;
import java.time.Instant;
import lombok.*;

/**
 * Persisted telemetry sample for mission history (Epic 4.5).
 *
 * <p>
 * Indexed on {@code (droneId, timestamp)} to keep historical range queries
 * for playback efficient. Uses a SEQUENCE id generator (rather than IDENTITY)
 * so Hibernate can batch inserts — IDENTITY forces a round-trip per row and
 * silently disables JDBC batching.
 */
@Entity
@Table(name = "telemetry_data", indexes = @Index(name = "idx_telemetry_drone_time", columnList = "droneId, timestamp"))
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TelemetryData {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "telemetry_seq")
    @SequenceGenerator(name = "telemetry_seq", sequenceName = "telemetry_data_seq", allocationSize = 50)
    private Long id;

    @Column(nullable = false)
    private String droneId;

    @Column(nullable = false)
    private Instant timestamp;

    // Location coordinates
    private Double latitude;
    private Double longitude;

    // Flight metrics
    private Double altitudeMeters;
    private Double speedMetersPerSecond;
    private Double headingDegrees;
    private Double batteryPercentage;
    private Integer satellites;
    private String flightMode;
    private Boolean armed;
}
