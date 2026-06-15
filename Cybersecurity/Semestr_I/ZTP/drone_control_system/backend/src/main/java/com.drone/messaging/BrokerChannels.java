package com.drone.messaging;

/**
 * Logical pub/sub channel names shared by the GCS backend and the MAVLink
 * adapter. Telemetry flows GCS-inbound; commands flow GCS-outbound; acks flow
 * back inbound to be routed to the originating operator.
 */
public final class BrokerChannels {

    /** Parsed telemetry published by the MAVLink adapter. */
    public static final String TELEMETRY = "gcs.telemetry";

    /** Validated drone commands forwarded from the command router. */
    public static final String COMMANDS = "gcs.commands";

    /** Command acknowledgements emitted by the MAVLink adapter. */
    public static final String ACKS = "gcs.acks";

    private BrokerChannels() {
    }
}
