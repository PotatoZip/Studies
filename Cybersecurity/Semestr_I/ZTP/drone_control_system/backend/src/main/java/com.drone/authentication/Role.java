package com.drone.authentication;

/**
 * Coarse-grained authorization roles for GCS operators.
 */
public enum Role {
    /** Full access: may issue commands and manage drones. */
    OPERATOR,
    /** Read-only access to telemetry, state and mission history. */
    VIEWER
}
