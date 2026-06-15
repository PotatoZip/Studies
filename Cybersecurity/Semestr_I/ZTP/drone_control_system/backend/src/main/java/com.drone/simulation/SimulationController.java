package com.drone.simulation;

import com.drone.common.exception.ResourceNotFoundException;
import com.drone.simulation.dto.SimulationRequest;
import com.drone.simulation.dto.SimulationRunStatus;
import jakarta.validation.Valid;
import java.security.Principal;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Temporary end-to-end simulation endpoint (Part 2). Triggers a scripted mission
 * that exercises the full pipeline — command router, mock MAVLink adapter, Redis
 * state, WebSocket broadcast, and PostgreSQL persistence — without any hardware.
 *
 * <p>Authenticated like every other API route; the issuing operator receives the
 * command ACKs on their {@code /user/queue/acks} WebSocket queue. Can be disabled
 * via {@code app.simulation.enabled=false}.
 */
@RestController
@RequestMapping("/api/simulation")
@RequiredArgsConstructor
public class SimulationController {

    private final MissionSimulationService simulationService;

    @Value("${app.simulation.enabled:true}")
    private boolean enabled;

    /** Start a full-pipeline mission simulation. Returns immediately with the run handle. */
    @PostMapping({"/start", "/full-pipeline"})
    public ResponseEntity<SimulationRunStatus> start(@Valid @RequestBody(required = false) SimulationRequest request,
                                                     Principal principal) {
        if (!enabled) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).build();
        }
        SimulationRequest req = request != null ? request : new SimulationRequest();
        SimulationRunStatus status = simulationService.start(req, principal.getName());
        return ResponseEntity.accepted().body(status);
    }

    /** Poll the status/result of a run. */
    @GetMapping("/{runId}")
    public SimulationRunStatus status(@PathVariable String runId) {
        return simulationService.get(runId)
                .orElseThrow(() -> ResourceNotFoundException.of("Simulation run", runId));
    }

    /** List all known runs (running + finished). */
    @GetMapping
    public List<SimulationRunStatus> list() {
        return simulationService.list();
    }

    /** Request an in-progress run to stop early. */
    @PostMapping("/{runId}/stop")
    public SimulationRunStatus stop(@PathVariable String runId) {
        return simulationService.stop(runId)
                .orElseThrow(() -> ResourceNotFoundException.of("Simulation run", runId));
    }
}
