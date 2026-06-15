package com.drone.websocket;

import java.security.Principal;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.messaging.SessionConnectedEvent;
import org.springframework.web.socket.messaging.SessionDisconnectEvent;

/**
 * Maintains {@link WebSocketSessionRegistry} from Spring's STOMP session
 * lifecycle events. Cleaning up on every disconnect — graceful or abrupt
 * (transport error, heartbeat timeout) — keeps session bookkeeping bounded and
 * gives a single place to release any session-scoped resources in future.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class WebSocketEventListener {

    private final WebSocketSessionRegistry registry;

    @EventListener
    public void onConnected(SessionConnectedEvent event) {
        StompHeaderAccessor accessor = StompHeaderAccessor.wrap(event.getMessage());
        String sessionId = accessor.getSessionId();
        Principal user = event.getUser();
        String username = user != null ? user.getName() : "anonymous";
        registry.register(sessionId, username);
        log.debug("WebSocket connected: session={} user={} (active={})",
                sessionId, username, registry.activeSessions());
    }

    @EventListener
    public void onDisconnect(SessionDisconnectEvent event) {
        String sessionId = event.getSessionId();
        String username = registry.remove(sessionId);
        log.debug("WebSocket disconnected: session={} user={} status={} (active={})",
                sessionId, username, event.getCloseStatus(), registry.activeSessions());
    }
}
