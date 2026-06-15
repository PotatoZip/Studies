package com.drone.mavlink.mock;

import com.drone.mavlink.dto.MavlinkCommandPacket;
import com.drone.mavlink.dto.MavlinkPacket;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ThreadLocalRandom;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Generates simulated drone flight data (the "sample mock data generator"
 * deliverable). Maintains a small physics-lite model per drone — position,
 * altitude, heading, battery — and advances it on each {@link #tick()}. It also
 * reacts to inbound commands so that issuing TAKEOFF/LAND/RTL/GOTO from the UI
 * produces visibly different telemetry.
 */
@Component
public class MockTelemetryGenerator {

    /** Base location the simulated fleet spawns around (central London). */
    private static final double BASE_LAT = 51.5074;
    private static final double BASE_LON = -0.1278;

    private final int droneCount;
    private final Map<Integer, DroneSim> fleet = new ConcurrentHashMap<>();

    public MockTelemetryGenerator(
            @Value("${app.mavlink.simulation.drone-count:3}") int droneCount) {
        this.droneCount = droneCount;
    }

    private synchronized void ensureInitialized() {
        if (!fleet.isEmpty()) {
            return;
        }
        for (int systemId = 1; systemId <= droneCount; systemId++) {
            DroneSim sim = new DroneSim();
            sim.systemId = systemId;
            sim.homeLat = BASE_LAT + (systemId * 0.002);
            sim.homeLon = BASE_LON + (systemId * 0.002);
            sim.lat = sim.homeLat;
            sim.lon = sim.homeLon;
            sim.altitude = 0;
            sim.targetAltitude = 0;
            sim.heading = ThreadLocalRandom.current().nextDouble(0, 360);
            sim.speed = 0;
            sim.battery = 100;
            sim.satellites = ThreadLocalRandom.current().nextInt(9, 13);
            sim.mode = "STABILIZE";
            sim.armed = false;
            fleet.put(systemId, sim);
        }
    }

    /** Advance every drone one simulation step and emit a packet for each. */
    public List<MavlinkPacket> tick() {
        ensureInitialized();
        List<MavlinkPacket> packets = new ArrayList<>(fleet.size());
        for (DroneSim sim : fleet.values()) {
            sim.advance();
            packets.add(sim.toPacket());
        }
        return packets;
    }

    /** Mutate a drone's state in response to a translated command. */
    public void applyCommand(MavlinkCommandPacket packet) {
        ensureInitialized();
        DroneSim sim = fleet.get(packet.targetSystem());
        if (sim == null) {
            return;
        }
        switch (packet.command()) {
            case MavlinkCommandPacket.MAV_CMD_COMPONENT_ARM_DISARM -> {
                sim.armed = packet.param1() == 1.0;
                sim.mode = sim.armed ? "GUIDED" : "STABILIZE";
            }
            case MavlinkCommandPacket.MAV_CMD_NAV_TAKEOFF -> {
                sim.armed = true;
                sim.mode = "TAKEOFF";
                sim.targetAltitude = packet.param7();
            }
            case MavlinkCommandPacket.MAV_CMD_NAV_LAND -> {
                sim.mode = "LAND";
                sim.targetAltitude = 0;
                sim.targetLat = null;
                sim.targetLon = null;
            }
            case MavlinkCommandPacket.MAV_CMD_NAV_RETURN_TO_LAUNCH -> {
                sim.mode = "RTL";
                sim.targetLat = sim.homeLat;
                sim.targetLon = sim.homeLon;
            }
            case MavlinkCommandPacket.MAV_CMD_NAV_WAYPOINT -> {
                sim.mode = "AUTO";
                sim.armed = true;
                sim.targetLat = packet.param5();
                sim.targetLon = packet.param6();
                sim.targetAltitude = packet.param7();
            }
            default -> { /* unknown command — no state change */ }
        }
    }

    /** Mutable per-drone simulation state. */
    private static final class DroneSim {
        int systemId;
        double homeLat, homeLon;
        double lat, lon;
        double altitude, targetAltitude;
        double heading, speed;
        double battery;
        int satellites;
        String mode;
        boolean armed;
        Double targetLat, targetLon;

        void advance() {
            // Battery slowly drains while armed, trickle-charges on the ground.
            if (armed) {
                battery = Math.max(0, battery - 0.05);
            } else if (battery < 100) {
                battery = Math.min(100, battery + 0.02);
            }

            // Converge altitude toward target.
            double altError = targetAltitude - altitude;
            altitude += Math.max(-2.0, Math.min(2.0, altError));
            if (altitude < 0.05) {
                altitude = 0;
            }

            // Navigate toward an active waypoint/home, else drift gently.
            if (targetLat != null && targetLon != null) {
                double dLat = targetLat - lat;
                double dLon = targetLon - lon;
                double dist = Math.hypot(dLat, dLon);
                if (dist < 0.0001) {
                    lat = targetLat;
                    lon = targetLon;
                    speed = 0;
                    if ("RTL".equals(mode)) {
                        targetAltitude = 0;
                    }
                    targetLat = null;
                    targetLon = null;
                } else {
                    double step = Math.min(dist, 0.0003);
                    lat += dLat / dist * step;
                    lon += dLon / dist * step;
                    heading = Math.toDegrees(Math.atan2(dLon, dLat));
                    if (heading < 0) {
                        heading += 360;
                    }
                    speed = 8 + ThreadLocalRandom.current().nextDouble(-1, 1);
                }
            } else if (armed && altitude > 1) {
                // Loiter: gentle heading wander.
                heading = (heading + ThreadLocalRandom.current().nextDouble(-5, 5) + 360) % 360;
                speed = Math.max(0, ThreadLocalRandom.current().nextDouble(0, 3));
                lat += Math.cos(Math.toRadians(heading)) * 0.00002;
                lon += Math.sin(Math.toRadians(heading)) * 0.00002;
            } else {
                speed = 0;
            }

            satellites = Math.max(6, Math.min(14,
                    satellites + ThreadLocalRandom.current().nextInt(-1, 2)));
        }

        MavlinkPacket toPacket() {
            return new MavlinkPacket(
                    systemId,
                    MavlinkPacket.COMPOSITE_TELEMETRY,
                    Instant.now(),
                    round(lat, 6),
                    round(lon, 6),
                    round(altitude, 2),
                    round(speed, 2),
                    round(heading, 1),
                    round(battery, 1),
                    satellites,
                    mode,
                    armed);
        }

        private static double round(double value, int decimals) {
            double factor = Math.pow(10, decimals);
            return Math.round(value * factor) / factor;
        }
    }
}
