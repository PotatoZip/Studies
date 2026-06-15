package com.drone.drone;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class DroneService {

    private final DroneRepository droneRepository;

    public Drone createDrone(Drone request) {
        Drone drone = Drone.builder()
                .id(UUID.randomUUID())
                .name(request.getName())
                .model(request.getModel())
                .serialNumber(request.getSerialNumber())
                .status(DroneStatus.IDLE)
                .lastSeen(Instant.now())
                .build();

        return droneRepository.save(drone);
    }

    public List<Drone> getAllDrones() {
        return droneRepository.findAll();
    }

    public Drone getDroneById(UUID id) {
        return droneRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Drone not found"));
    }

    public Drone updateDroneStatus(UUID id, DroneStatus status) {
        Drone drone = droneRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Drone not found"));

        drone.setStatus(status);
        drone.setLastSeen(Instant.now());

        return droneRepository.save(drone);
    }

    public void deleteDrone(UUID id) {
        droneRepository.deleteById(id);
    }
}