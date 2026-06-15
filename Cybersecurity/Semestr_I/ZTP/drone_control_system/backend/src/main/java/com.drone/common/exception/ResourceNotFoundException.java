package com.drone.common.exception;

/**
 * Thrown when a requested entity (drone, mission, telemetry record, ...) does
 * not exist. Mapped to HTTP 404 by {@link GlobalExceptionHandler}.
 */
public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String message) {
        super(message);
    }

    public static ResourceNotFoundException of(String entity, Object id) {
        return new ResourceNotFoundException(entity + " not found: " + id);
    }
}
