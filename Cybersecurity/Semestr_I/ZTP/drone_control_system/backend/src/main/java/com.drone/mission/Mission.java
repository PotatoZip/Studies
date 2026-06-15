package com.drone.mission;

import com.drone.drone.Drone;
import jakarta.persistence.*;
import lombok.*;
import java.time.Instant;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "missions")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Mission {
    @Id
    private UUID id;
    private String name;

    @Enumerated(EnumType.STRING)
    private MissionStatus status;

    private Instant startedAt;
    private Instant endedAt;

    @ManyToMany
    @JoinTable(name = "mission_drones", joinColumns = @JoinColumn(name = "mission_id"), inverseJoinColumns = @JoinColumn(name = "drone_id"))
    @Builder.Default
    private Set<Drone> drones = new HashSet<>();
}
