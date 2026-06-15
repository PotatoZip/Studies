package com.drone.websocket;

import com.drone.security.JwtService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;
import org.springframework.messaging.support.MessageHeaderAccessor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;

/**
 * Authenticates STOMP sessions on the CONNECT frame (Epic 4.1). The client
 * passes the same JWT it uses for REST as a {@code Authorization: Bearer ...}
 * native STOMP header; this interceptor validates it and binds the resulting
 * principal to the session. Per-user destinations ({@code /user/queue/...})
 * then resolve to that principal, which is how command acks reach the specific
 * operator who issued the command.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class StompAuthChannelInterceptor implements ChannelInterceptor {

    private final JwtService jwtService;

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        StompHeaderAccessor accessor =
                MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);

        if (accessor != null && StompCommand.CONNECT.equals(accessor.getCommand())) {
            String token = resolveToken(accessor);
            String username = token != null ? jwtService.extractUsername(token) : null;
            if (username == null) {
                throw new IllegalArgumentException("Unauthenticated WebSocket connection rejected");
            }
            String role = "ROLE_OPERATOR";
            UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(
                    username, null, List.of(new SimpleGrantedAuthority(role)));
            accessor.setUser(auth);
            log.debug("Authenticated WebSocket session for '{}'", username);
        }
        return message;
    }

    private String resolveToken(StompHeaderAccessor accessor) {
        List<String> authHeaders = accessor.getNativeHeader("Authorization");
        if (authHeaders != null && !authHeaders.isEmpty()) {
            String header = authHeaders.get(0);
            if (header != null && header.startsWith("Bearer ")) {
                return header.substring(7);
            }
        }
        return null;
    }
}
