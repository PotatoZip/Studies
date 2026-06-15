package com.drone.authentication;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Payload for {@code POST /api/v1/auth/login}.
 */
@Data
public class LoginRequest {

    @NotBlank(message = "Username is required")
    private String username;

    @NotBlank(message = "Password is required")
    private String password;
}
