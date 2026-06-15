package com.drone.mavlink;

import com.drone.mavlink.dto.MavlinkAckPacket;
import com.drone.mavlink.dto.MavlinkCommandPacket;
import com.drone.mavlink.dto.MavlinkPacket;
import java.util.function.Consumer;

/**
 * MAVLink connection layer (Epic 3.1): the transport that talks to a PX4 /
 * ArduPilot flight controller over UDP/TCP. This interface intentionally hides
 * the wire details so the rest of the GCS depends only on the abstraction; the
 * shipped implementation is {@code MockMavlinkConnection}.
 */
public interface MavlinkConnection {

    /** Open the underlying transport (bind UDP socket / open TCP stream). */
    void connect();

    /** Close the transport and release resources. */
    void disconnect();

    boolean isConnected();

    /** Send a command packet to a flight controller. */
    void send(MavlinkCommandPacket packet);

    /** Register the handler invoked for every inbound telemetry packet. */
    void onPacket(Consumer<MavlinkPacket> handler);

    /** Register the handler invoked for every inbound command acknowledgement. */
    void onAck(Consumer<MavlinkAckPacket> handler);
}
