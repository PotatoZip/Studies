package com.drone.mission;

import com.drone.drone.Drone;
import com.drone.drone.DroneRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class MissionService {

    private final MissionRepository missionRepository;
    private final DroneRepository droneRepository;

    public MissionResponse create(MissionRequest request) {
        Mission mission = Mission.builder()
                .id(UUID.randomUUID())
                .name(request.getName())
                .status(MissionStatus.PLANNED)
                .build();

        // Optionally assign drones up-front; null/empty leaves the mission unassigned.
        if (request.getDroneIds() != null) {
            for (UUID droneId : request.getDroneIds()) {
                Drone drone = droneRepository.findById(droneId)
                        .orElseThrow(() -> new RuntimeException("Drone not found: " + droneId));
                mission.getDrones().add(drone);
            }
        }

        missionRepository.save(mission);

        return mapToResponse(mission);
    }

    public List<MissionResponse> getAllMissions() {
        return missionRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    public MissionResponse getById(UUID missionId) {
        return mapToResponse(getMissionOrThrow(missionId));
    }

    public void assignDroneToMission(UUID missionId, UUID droneId) {

        Mission mission = getMissionOrThrow(missionId);
        Drone drone = droneRepository.findById(droneId)
                .orElseThrow(() -> new RuntimeException("Drone not found"));

        if (mission.getDrones().contains(drone)) {
            throw new RuntimeException("Drone already assigned");
        }

        mission.getDrones().add(drone);
        missionRepository.save(mission);
    }

    public MissionResponse startMission(UUID missionId) {

        Mission mission = getMissionOrThrow(missionId);

        if (mission.getDrones().isEmpty()) {
            throw new RuntimeException("Mission has no drones");
        }

        if (mission.getStatus() != MissionStatus.PLANNED) {
            throw new RuntimeException("Mission cannot be started");
        }

        mission.setStatus(MissionStatus.RUNNING);
        mission.setStartedAt(Instant.now());

        missionRepository.save(mission);

        return mapToResponse(mission);
    }

    public MissionResponse stopMission(UUID missionId) {

        Mission mission = getMissionOrThrow(missionId);

        if (mission.getStatus() != MissionStatus.RUNNING) {
            throw new RuntimeException("Mission is not running");
        }

        mission.setStatus(MissionStatus.COMPLETED);
        mission.setEndedAt(Instant.now());

        missionRepository.save(mission);

        return mapToResponse(mission);
    }

    public void deleteMission(UUID missionId) {
        Mission mission = getMissionOrThrow(missionId);

        if (mission.getStatus() == MissionStatus.RUNNING) {
            throw new RuntimeException("Cannot delete running mission");
        }

        missionRepository.delete(mission);
    }

    // HELPERS

    private Mission getMissionOrThrow(UUID id) {
        return missionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Mission not found"));
    }

    private MissionResponse mapToResponse(Mission mission) {
        return new MissionResponse(
                mission.getId(),
                mission.getName(),
                mission.getStatus(),
                mission.getDrones()
                        .stream()
                        .map(Drone::getId)
                        .collect(Collectors.toSet()));
    }
}