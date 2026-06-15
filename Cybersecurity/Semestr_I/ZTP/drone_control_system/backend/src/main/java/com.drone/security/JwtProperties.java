package com.drone.security;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Externalized JWT settings bound from {@code app.jwt.*}.
 *
 * @param secret      HMAC signing secret; must be at least 256 bits (32 chars)
 *                    for HS256. Supply via the {@code APP_JWT_SECRET} env var in
 *                    production.
 * @param expirationMs token lifetime in milliseconds
 */
@ConfigurationProperties(prefix = "app.jwt")
public record JwtProperties(String secret, long expirationMs) {
}
