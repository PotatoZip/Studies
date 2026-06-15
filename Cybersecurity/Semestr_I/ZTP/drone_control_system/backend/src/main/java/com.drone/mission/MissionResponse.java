package com.drone.mission;

import lombok.*;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MissionResponse {
    private UUID id;
    private String name;
    private MissionStatus status;
    private Set<UUID> droneIds;
}
