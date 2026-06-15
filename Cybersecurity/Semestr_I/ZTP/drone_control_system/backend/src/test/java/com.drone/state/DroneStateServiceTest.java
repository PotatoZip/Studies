package com.drone.state;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.drone.messaging.MessageBroker;
import com.drone.telemetry.dto.TelemetryMessage;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.data.redis.core.script.RedisScript;

@ExtendWith(MockitoExtension.class)
class DroneStateServiceTest {

    @Mock private StringRedisTemplate redis;
    @Mock private ValueOperations<String, String> valueOps;
    @Mock private MessageBroker messageBroker;

    private ObjectMapper objectMapper;
    private DroneStateService service;

    @BeforeEach
    void setUp() {
        objectMapper = new ObjectMapper().registerModule(new JavaTimeModule());
        service = new DroneStateService(redis, objectMapper, messageBroker, 30L);
    }

    private TelemetryMessage telemetry(String droneId) {
        return new TelemetryMessage(droneId, Instant.parse("2026-06-01T00:00:00Z"),
                51.5, -0.12, 100.0, 5.0, 90.0, 80.0, 11, "AUTO", true);
    }

    @Test
    void updateWritesSnapshotViaAtomicCasScript() {
        TelemetryMessage t = telemetry("drone-1");
        long version = t.timestamp().toEpochMilli();

        service.update(t);

        // Versioned write: state + version keys, version arg, and TTL in millis,
        // executed atomically as a single Lua script (compare-and-set).
        verify(redis).execute(
                any(RedisScript.class),
                eq(List.of("drone:state:drone-1", "drone:ver:drone-1")),
                eq(Long.toString(version)),
                anyString(),
                eq("30000"));
    }

    @Test
    void getStateDeserializesStoredSnapshot() throws Exception {
        when(redis.opsForValue()).thenReturn(valueOps);
        DroneState stored = DroneState.from(telemetry("drone-1"));
        when(valueOps.get("drone:state:drone-1"))
                .thenReturn(objectMapper.writeValueAsString(stored));

        var result = service.getState("drone-1");

        assertThat(result).isPresent();
        assertThat(result.get().droneId()).isEqualTo("drone-1");
        assertThat(result.get().latest().flightMode()).isEqualTo("AUTO");
        assertThat(result.get().latest().armed()).isTrue();
    }

    @Test
    void getStateReturnsEmptyWhenAbsentOrExpired() {
        when(redis.opsForValue()).thenReturn(valueOps);
        when(valueOps.get("drone:state:ghost")).thenReturn(null);

        assertThat(service.getState("ghost")).isEmpty();
    }

    @Test
    void getAllStatesReturnsEmptyWhenNoKeys() {
        when(redis.keys("drone:state:*")).thenReturn(Set.of());

        assertThat(service.getAllStates()).isEmpty();
    }

    @Test
    void getAllStatesDeserializesEachKey() throws Exception {
        when(redis.opsForValue()).thenReturn(valueOps);
        when(redis.keys("drone:state:*"))
                .thenReturn(Set.of("drone:state:drone-1", "drone:state:drone-2"));
        when(valueOps.multiGet(any())).thenReturn(List.of(
                objectMapper.writeValueAsString(DroneState.from(telemetry("drone-1"))),
                objectMapper.writeValueAsString(DroneState.from(telemetry("drone-2")))));

        List<DroneState> states = service.getAllStates();

        assertThat(states).hasSize(2);
        assertThat(states).extracting(DroneState::droneId)
                .containsExactlyInAnyOrder("drone-1", "drone-2");
    }
}
