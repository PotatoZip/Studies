package com.drone.drone;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/drones")
@RequiredArgsConstructor
public class DronesController {

    private final DroneService droneService;

    @PostMapping
    public Drone createDrone(@RequestBody Drone request) {
        return droneService.createDrone(request);
    }

    @GetMapping
    public List<Drone> getAllDrones() {
        return droneService.getAllDrones();
    }

    @GetMapping("/{id}")
    public Drone getDroneById(@PathVariable UUID id) {
        return droneService.getDroneById(id);
    }

    @PatchMapping("/{id}/status")
    public Drone updateDroneStatus(
            @PathVariable UUID id,
            @RequestParam DroneStatus status) {
        return droneService.updateDroneStatus(id, status);
    }

    @DeleteMapping("/{id}")
    public void deleteDrone(@PathVariable UUID id) {
        droneService.deleteDrone(id);
    }
}