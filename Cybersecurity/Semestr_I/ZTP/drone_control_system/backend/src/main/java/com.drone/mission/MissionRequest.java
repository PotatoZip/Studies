package com.drone.mission;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import java.util.Set;
import java.util.UUID;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class MissionRequest {

    @NotBlank(message = "Mission name is required")
    private String name;

    @NotEmpty(message = "At least one drone must be assigned to the mission")
    private Set<UUID> droneIds;
}
