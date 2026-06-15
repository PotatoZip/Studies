package com.drone.common.exception;

/**
 * Thrown by the command-router validation layer when a drone command is
 * malformed or not allowed for the drone's current state. Mapped to HTTP 400.
 */
public class InvalidCommandException extends RuntimeException {

    public InvalidCommandException(String message) {
        super(message);
    }
}
