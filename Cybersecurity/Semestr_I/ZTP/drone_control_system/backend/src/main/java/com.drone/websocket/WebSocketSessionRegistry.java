package com.drone.websocket;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Component;

/**
 * Tracks live STOMP sessions (sessionId → username) so the gateway has an
 * authoritative, bounded view of who is connected. Entries are added on
 * CONNECT and removed on DISCONNECT by {@link WebSocketEventListener}, which is
 * what prevents per-session bookkeeping from leaking when clients drop
 * unexpectedly.
 */
@Component
public class WebSocketSessionRegistry {

    private final Map<String, String> sessions = new ConcurrentHashMap<>();

    public void register(String sessionId, String username) {
        if (sessionId != null && username != null) {
            sessions.put(sessionId, username);
        }
    }

    /** Remove a session; returns the username it belonged to (or null). */
    public String remove(String sessionId) {
        return sessionId == null ? null : sessions.remove(sessionId);
    }

    public int activeSessions() {
        return sessions.size();
    }

    public Set<String> activeUsers() {
        return Set.copyOf(sessions.values());
    }
}
