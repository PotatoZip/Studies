package com.drone.command;

/**
 * Lifecycle of a command as it moves through the router and broker.
 */
public enum CommandStatus {
    /** Accepted by the router, awaiting dispatch to the broker. */
    QUEUED,
    /** Published to the broker for the MAVLink adapter. */
    SENT,
    /** Adapter acknowledged successful execution. */
    ACKNOWLEDGED,
    /** Adapter rejected the command. */
    REJECTED,
    /** No ack received within the timeout window. */
    TIMEOUT
}
