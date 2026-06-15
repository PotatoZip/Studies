package com.drone.authentication;

import lombok.Builder;
import lombok.Data;

/**
 * Returned by register/login. Carries the JWT the client attaches to REST calls
 * ({@code Authorization: Bearer <token>}) and the WebSocket STOMP CONNECT frame.
 */
@Data
@Builder
public class AuthResponse {
    private String token;
    private String tokenType;
    private long expiresInMs;
    private String username;
    private Role role;
}
