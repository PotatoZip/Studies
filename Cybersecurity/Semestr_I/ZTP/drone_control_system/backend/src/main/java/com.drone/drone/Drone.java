package com.drone.drone;

import jakarta.persistence.*;
import lombok.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "drones")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Drone {
    @Id
    private UUID id;
    private String name;
    private String model;
    private String serialNumber;

    @Enumerated(EnumType.STRING)
    private DroneStatus status;

    private Instant lastSeen;
}
