package com.drone.simulation;

import com.drone.command.CommandType;
import com.drone.command.dto.CommandRequest;
import com.drone.command.dto.CommandResponse;
import com.drone.command.CommandService;
import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import com.drone.simulation.dto.SimulationRequest;
import com.drone.simulation.dto.SimulationRunStatus;
import com.drone.telemetry.dto.TelemetryMessage;
import com.drone.telemetry.service.TelemetryBatchWriter;
import jakarta.annotation.PreDestroy;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * Drives a scripted, hardware-free mission through the <b>real</b> GCS pipeline
 * (Part 2 of the integration task). For each phase it:
 * <ol>
 *   <li>issues the command through the actual {@link CommandService} router
 *       (validation → queue → broker → mock MAVLink adapter → ACK back to the
 *       requesting operator);</li>
 *   <li>publishes generated telemetry to the broker's telemetry channel, which
 *       fans out to the Redis "Latest State" cache, the WebSocket broadcaster
 *       (live push to connected clients), and the batch-persistence buffer.</li>
 * </ol>
 *
 * Profile: ARM → TAKEOFF → WAYPOINT → RTL → LAND → DISARM. Runs asynchronously;
 * callers poll {@link #get(String)} for progress.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class MissionSimulationService {

    private static final double BASE_LAT = 51.5074;
    private static final double BASE_LON = -0.1278;

    private final CommandService commandService;
    private final MessageBroker messageBroker;
    private final TelemetryBatchWriter batchWriter;

    private final Map<String, SimulationRun> runs = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newCachedThreadPool(r -> {
        Thread t = new Thread(r, "mission-sim");
        t.setDaemon(true);
        return t;
    });

    public SimulationRunStatus start(SimulationRequest request, String issuedBy) {
        SimulationRun run = new SimulationRun(
                UUID.randomUUID().toString(),
                orDefault(request.getDroneId(), "drone-901"));
        runs.put(run.runId, run);
        executor.submit(() -> runMission(run, request, issuedBy));
        log.info("Started mission simulation {} for {} (by {})", run.runId, run.droneId, issuedBy);
        return run.toStatus();
    }

    public Optional<SimulationRunStatus> get(String runId) {
        return Optional.ofNullable(runs.get(runId)).map(SimulationRun::toStatus);
    }

    public Optional<SimulationRunStatus> stop(String runId) {
        SimulationRun run = runs.get(runId);
        if (run == null) {
            return Optional.empty();
        }
        run.stopRequested = true;
        return Optional.of(run.toStatus());
    }

    public List<SimulationRunStatus> list() {
        return runs.values().stream().map(SimulationRun::toStatus).toList();
    }

    // ── Mission loop ───────────────────────────────────────────────────────────

    private void runMission(SimulationRun run, SimulationRequest req, String issuedBy) {
        int rateHz = clamp(orDefault(req.getRateHz(), 10), 1, 50);
        int phaseSeconds = clamp(orDefault(req.getPhaseSeconds(), 4), 1, 60);
        double takeoffAlt = orDefault(req.getTakeoffAltitudeMeters(), 50.0);
        double cruiseAlt = orDefault(req.getCruiseAltitudeMeters(), 80.0);
        double homeLat = orDefault(req.getHomeLatitude(), BASE_LAT);
        double homeLon = orDefault(req.getHomeLongitude(), BASE_LON);
        double wpLat = orDefault(req.getWaypointLatitude(), homeLat + 0.01);
        double wpLon = orDefault(req.getWaypointLongitude(), homeLon + 0.01);

        FlightModel model = new FlightModel(homeLat, homeLon);

        try {
            // ARM
            run.currentPhase = "ARM";
            issueCommand(run, CommandType.ARM, null, null, null, issuedBy);
            model.armed = true;
            model.mode = "GUIDED";
            emitFor(run, model, 1, rateHz);

            // TAKEOFF — climb to target altitude
            run.currentPhase = "TAKEOFF";
            issueCommand(run, CommandType.TAKEOFF, takeoffAlt, null, null, issuedBy);
            model.mode = "TAKEOFF";
            model.targetAlt = takeoffAlt;
            emitFor(run, model, phaseSeconds, rateHz);

            // WAYPOINT — navigate to waypoint at cruise altitude
            run.currentPhase = "WAYPOINT";
            issueCommand(run, CommandType.GOTO_WAYPOINT, cruiseAlt, wpLat, wpLon, issuedBy);
            model.mode = "AUTO";
            model.targetAlt = cruiseAlt;
            model.targetLat = wpLat;
            model.targetLon = wpLon;
            emitFor(run, model, phaseSeconds, rateHz);

            // RTL — return to launch
            run.currentPhase = "RTL";
            issueCommand(run, CommandType.RTL, null, null, null, issuedBy);
            model.mode = "RTL";
            model.targetLat = homeLat;
            model.targetLon = homeLon;
            emitFor(run, model, phaseSeconds, rateHz);

            // LAND — descend to ground
            run.currentPhase = "LAND";
            issueCommand(run, CommandType.LAND, null, null, null, issuedBy);
            model.mode = "LAND";
            model.targetAlt = 0.0;
            model.targetLat = null;
            model.targetLon = null;
            emitFor(run, model, phaseSeconds, rateHz);

            // DISARM
            run.currentPhase = "DISARM";
            issueCommand(run, CommandType.DISARM, null, null, null, issuedBy);
            model.armed = false;
            model.mode = "STABILIZE";
            emitFor(run, model, 1, rateHz);

            run.currentPhase = "DONE";
            run.state = run.stopRequested ? "STOPPED" : "COMPLETED";
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            run.state = "STOPPED";
        } catch (Exception e) {
            log.error("Simulation {} failed: {}", run.runId, e.getMessage(), e);
            run.state = "FAILED";
            run.message = e.getMessage();
        } finally {
            run.finishedAt = Instant.now();
            // Force persistence so the full flight log lands in the DB promptly.
            batchWriter.flush();
            log.info("Simulation {} finished: state={} samples={}",
                    run.runId, run.state, run.samples.get());
        }
    }

    private void issueCommand(SimulationRun run, CommandType type, Double alt,
                              Double lat, Double lon, String issuedBy) {
        CommandRequest cmd = new CommandRequest();
        cmd.setDroneId(run.droneId);
        cmd.setType(type);
        cmd.setAltitudeMeters(alt);
        cmd.setLatitude(lat);
        cmd.setLongitude(lon);
        cmd.setClientRequestId("sim-" + run.runId + "-" + type);
        CommandResponse response = commandService.submit(cmd, issuedBy);
        run.commandIds.add(response.getCommandId());
    }

    /** Emit telemetry at {@code rateHz} for {@code seconds}, advancing the model. */
    private void emitFor(SimulationRun run, FlightModel model, int seconds, int rateHz)
            throws InterruptedException {
        int ticks = seconds * rateHz;
        long sleepMs = 1000L / rateHz;
        double dt = 1.0 / rateHz;
        for (int i = 0; i < ticks && !run.stopRequested; i++) {
            model.step(dt);
            messageBroker.publish(BrokerChannels.TELEMETRY, model.toTelemetry(run.droneId));
            run.samples.incrementAndGet();
            Thread.sleep(sleepMs);
        }
    }

    @PreDestroy
    void shutdown() {
        executor.shutdownNow();
    }

    // ── Helpers ─────────────────────────────────────────────────────────────────

    private static <T> T orDefault(T value, T fallback) {
        return value != null ? value : fallback;
    }

    private static int clamp(int v, int min, int max) {
        return Math.max(min, Math.min(max, v));
    }

    // ── Internal run state ───────────────────────────────────────────────────────

    private static final class SimulationRun {
        final String runId;
        final String droneId;
        final Instant startedAt = Instant.now();
        final AtomicInteger samples = new AtomicInteger();
        final List<String> commandIds = new CopyOnWriteArrayList<>();
        volatile String state = "RUNNING";
        volatile String currentPhase = "INIT";
        volatile Instant finishedAt;
        volatile String message;
        volatile boolean stopRequested;

        SimulationRun(String runId, String droneId) {
            this.runId = runId;
            this.droneId = droneId;
        }

        SimulationRunStatus toStatus() {
            return new SimulationRunStatus(runId, droneId, state, currentPhase,
                    startedAt, finishedAt, samples.get(), List.copyOf(commandIds), message);
        }
    }

    // ── Lightweight flight model ──────────────────────────────────────────────────

    private static final class FlightModel {
        double lat, lon, alt, heading, speed, battery = 100;
        int satellites = 12;
        String mode = "STABILIZE";
        boolean armed;
        Double targetLat, targetLon, targetAlt = 0.0;

        FlightModel(double homeLat, double homeLon) {
            this.lat = homeLat;
            this.lon = homeLon;
        }

        void step(double dt) {
            if (armed) {
                battery = Math.max(0, battery - 0.05);
            }
            // Converge altitude (max ~5 m/s climb/descent).
            if (targetAlt != null) {
                double err = targetAlt - alt;
                alt += Math.max(-5 * dt, Math.min(5 * dt, err));
                if (alt < 0.05) alt = 0;
            }
            // Navigate toward an active target.
            if (targetLat != null && targetLon != null) {
                double dLat = targetLat - lat;
                double dLon = targetLon - lon;
                double dist = Math.hypot(dLat, dLon);
                if (dist < 1e-5) {
                    lat = targetLat;
                    lon = targetLon;
                    speed = 0;
                } else {
                    double step = Math.min(dist, 0.0006 * dt * 10); // ~ move per tick
                    lat += dLat / dist * step;
                    lon += dLon / dist * step;
                    heading = (Math.toDegrees(Math.atan2(dLon, dLat)) + 360) % 360;
                    speed = 12;
                }
            } else {
                speed = 0;
            }
        }

        TelemetryMessage toTelemetry(String droneId) {
            return new TelemetryMessage(
                    droneId, Instant.now(),
                    round(lat, 6), round(lon, 6), round(alt, 2), round(speed, 2),
                    round(heading, 1), round(battery, 1), satellites, mode, armed);
        }

        private static double round(double v, int decimals) {
            double f = Math.pow(10, decimals);
            return Math.round(v * f) / f;
        }
    }
}
