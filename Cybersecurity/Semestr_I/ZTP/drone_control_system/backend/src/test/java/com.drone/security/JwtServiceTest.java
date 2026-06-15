package com.drone.security;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class JwtServiceTest {

    private JwtService jwtService;

    @BeforeEach
    void setUp() {
        // 32+ char secret so HS256/384 key requirements are satisfied.
        JwtProperties props = new JwtProperties(
                "test-secret-key-that-is-at-least-256-bits-long-000", 3_600_000L);
        jwtService = new JwtService(props);
    }

    @Test
    void generatesTokenAndExtractsSubject() {
        String token = jwtService.generateToken("operator1", "OPERATOR");

        assertThat(token).isNotBlank();
        assertThat(jwtService.isValid(token)).isTrue();
        assertThat(jwtService.extractUsername(token)).isEqualTo("operator1");
        assertThat(jwtService.getExpirationMs()).isEqualTo(3_600_000L);
    }

    @Test
    void rejectsGarbageToken() {
        assertThat(jwtService.isValid("not.a.jwt")).isFalse();
        assertThat(jwtService.extractUsername("not.a.jwt")).isNull();
    }

    @Test
    void rejectsTokenSignedWithDifferentSecret() {
        String foreign = new JwtService(new JwtProperties(
                "a-completely-different-secret-key-also-256-bits-x", 3_600_000L))
                .generateToken("intruder", "OPERATOR");

        assertThat(jwtService.isValid(foreign)).isFalse();
    }

    @Test
    void treatsExpiredTokenAsInvalid() {
        JwtService shortLived = new JwtService(new JwtProperties(
                "test-secret-key-that-is-at-least-256-bits-long-000", -1L));
        String expired = shortLived.generateToken("operator1", "OPERATOR");

        assertThat(shortLived.isValid(expired)).isFalse();
    }
}
