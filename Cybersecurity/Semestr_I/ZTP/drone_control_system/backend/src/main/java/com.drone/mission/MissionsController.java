package com.drone.mission;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/missions")
@RequiredArgsConstructor
public class MissionsController {

    private final MissionService missionService;

    @GetMapping
    public List<MissionResponse> getAllMissions() {
        return missionService.getAllMissions();
    }

    // szczegóły misji
    @GetMapping("/{id}")
    public MissionResponse getMission(@PathVariable UUID id) {
        return missionService.getById(id);
    }

    @PostMapping
    public MissionResponse createMission(@Valid @RequestBody MissionRequest request) {
        return missionService.create(request);
    }

    // przypisanie drona do misji
    @PostMapping("/{missionId}/drones/{droneId}")
    public void assignDroneToMission(
            @PathVariable UUID missionId,
            @PathVariable UUID droneId) {
        missionService.assignDroneToMission(missionId, droneId);
    }

    @PostMapping("/{id}/start")
    public MissionResponse startMission(@PathVariable UUID id) {
        return missionService.startMission(id);
    }

    @PostMapping("/{id}/stop")
    public MissionResponse stopMission(@PathVariable UUID id) {
        return missionService.stopMission(id);
    }

    @DeleteMapping("/{id}")
    public void deleteMission(@PathVariable UUID id) {
        missionService.deleteMission(id);
    }
}