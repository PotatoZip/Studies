package com.drone.state;

import com.drone.common.exception.ResourceNotFoundException;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Read access to the live "Latest State" cache. Useful for a dashboard to
 * bootstrap the current fleet before the WebSocket stream takes over.
 */
@RestController
@RequestMapping("/api/v1/drones/state")
@RequiredArgsConstructor
public class DroneStateController {

    private final DroneStateService stateService;

    /** All drones currently online (have non-expired state). */
    @GetMapping
    public List<DroneState> getAll() {
        return stateService.getAllStates();
    }

    @GetMapping("/{droneId}")
    public DroneState getOne(@PathVariable String droneId) {
        return stateService.getState(droneId)
                .orElseThrow(() -> ResourceNotFoundException.of("Drone state", droneId));
    }
}
