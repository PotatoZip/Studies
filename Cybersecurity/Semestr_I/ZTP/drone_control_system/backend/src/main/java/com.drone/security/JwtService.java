package com.drone.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.Map;
import javax.crypto.SecretKey;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * Issues and validates HMAC-signed JWTs (JJWT 0.12.x). Used by both the REST
 * authentication filter and the WebSocket STOMP CONNECT interceptor, so the
 * same token authorizes HTTP and WebSocket access.
 */
@Slf4j
@Service
public class JwtService {

    private final SecretKey key;
    private final long expirationMs;

    public JwtService(JwtProperties properties) {
        this.key = Keys.hmacShaKeyFor(properties.secret().getBytes(StandardCharsets.UTF_8));
        this.expirationMs = properties.expirationMs();
    }

    /** Generate a signed token for the given username carrying its role. */
    public String generateToken(String username, String role) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + expirationMs);
        return Jwts.builder()
                .subject(username)
                .claims(Map.of("role", role))
                .issuedAt(now)
                .expiration(expiry)
                .signWith(key)
                .compact();
    }

    public long getExpirationMs() {
        return expirationMs;
    }

    /** Extract the username (subject), or {@code null} if the token is invalid. */
    public String extractUsername(String token) {
        Claims claims = parse(token);
        return claims == null ? null : claims.getSubject();
    }

    /** @return true if the token is well-formed, correctly signed and unexpired. */
    public boolean isValid(String token) {
        return parse(token) != null;
    }

    private Claims parse(String token) {
        try {
            return Jwts.parser()
                    .verifyWith(key)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
        } catch (Exception e) {
            log.debug("Invalid JWT: {}", e.getMessage());
            return null;
        }
    }
}
