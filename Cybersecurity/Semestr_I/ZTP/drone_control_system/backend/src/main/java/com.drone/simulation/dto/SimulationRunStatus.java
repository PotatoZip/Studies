package com.drone.simulation.dto;

import java.time.Instant;
import java.util.List;

/**
 * Public status/result view of a simulation run.
 */
public record SimulationRunStatus(
        String runId,
        String droneId,
        String state,        // RUNNING | COMPLETED | STOPPED | FAILED
        String currentPhase, // ARM | TAKEOFF | WAYPOINT | RTL | LAND | DISARM | DONE
        Instant startedAt,
        Instant finishedAt,
        int telemetrySamples,
        List<String> commandIds,
        String message
) {
}
