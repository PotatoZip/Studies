package com.drone.authentication;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.drone.security.JwtService;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock private UserRepository userRepository;
    @Mock private PasswordEncoder passwordEncoder;
    @Mock private AuthenticationManager authenticationManager;
    @Mock private JwtService jwtService;

    @InjectMocks private AuthService authService;

    private RegisterRequest registerRequest;

    @BeforeEach
    void setUp() {
        registerRequest = new RegisterRequest();
        registerRequest.setUsername("operator1");
        registerRequest.setEmail("op1@example.com");
        registerRequest.setPassword("password123");
    }

    @Test
    void registerHashesPasswordAndReturnsToken() {
        when(userRepository.existsByUsername("operator1")).thenReturn(false);
        when(passwordEncoder.encode("password123")).thenReturn("hashed");
        when(jwtService.generateToken("operator1", "OPERATOR")).thenReturn("jwt-token");
        when(jwtService.getExpirationMs()).thenReturn(86_400_000L);

        AuthResponse response = authService.register(registerRequest);

        assertThat(response.getToken()).isEqualTo("jwt-token");
        assertThat(response.getTokenType()).isEqualTo("Bearer");
        assertThat(response.getUsername()).isEqualTo("operator1");
        assertThat(response.getRole()).isEqualTo(Role.OPERATOR);

        verify(userRepository).save(any(User.class));
        verify(passwordEncoder).encode("password123");
    }

    @Test
    void registerDefaultsRoleToOperatorWhenAbsent() {
        when(userRepository.existsByUsername(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("hashed");
        when(jwtService.generateToken(anyString(), anyString())).thenReturn("t");

        AuthResponse response = authService.register(registerRequest);

        assertThat(response.getRole()).isEqualTo(Role.OPERATOR);
    }

    @Test
    void registerRejectsDuplicateUsername() {
        when(userRepository.existsByUsername("operator1")).thenReturn(true);

        assertThatThrownBy(() -> authService.register(registerRequest))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("already taken");

        verify(userRepository, never()).save(any());
    }

    @Test
    void loginAuthenticatesAndReturnsToken() {
        LoginRequest login = new LoginRequest();
        login.setUsername("operator1");
        login.setPassword("password123");

        User user = User.builder().username("operator1").role(Role.VIEWER).build();
        when(userRepository.findByUsername("operator1")).thenReturn(Optional.of(user));
        when(jwtService.generateToken("operator1", "VIEWER")).thenReturn("jwt-token");

        AuthResponse response = authService.login(login);

        assertThat(response.getToken()).isEqualTo("jwt-token");
        assertThat(response.getRole()).isEqualTo(Role.VIEWER);
        verify(authenticationManager).authenticate(any(UsernamePasswordAuthenticationToken.class));
    }

    @Test
    void loginPropagatesBadCredentials() {
        LoginRequest login = new LoginRequest();
        login.setUsername("operator1");
        login.setPassword("wrong");

        when(authenticationManager.authenticate(any()))
                .thenThrow(new BadCredentialsException("bad"));

        assertThatThrownBy(() -> authService.login(login))
                .isInstanceOf(BadCredentialsException.class);
        verify(jwtService, never()).generateToken(anyString(), anyString());
    }
}
