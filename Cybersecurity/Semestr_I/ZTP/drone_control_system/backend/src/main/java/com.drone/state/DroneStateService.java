package com.drone.state;

import com.drone.messaging.BrokerChannels;
import com.drone.messaging.MessageBroker;
import com.drone.telemetry.dto.TelemetryMessage;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.data.redis.core.script.RedisScript;
import org.springframework.stereotype.Service;

/**
 * Maintains the "Latest State" for every drone in Redis (Epic 4.2).
 *
 * <p>Each drone's most recent state is stored under {@code drone:state:<id>}
 * with a TTL, so a drone that stops sending telemetry expires and drops out of
 * the active fleet automatically.
 *
 * <p><b>Versioned writes:</b> telemetry can arrive out of order or concurrently
 * (multiple commands / broker listener threads). To avoid a newer snapshot being
 * clobbered by a late-arriving older one, updates go through an atomic Lua
 * compare-and-set keyed on the sample timestamp (a monotonic version): the state
 * is written only when the incoming timestamp is &ge; the stored version. The
 * check and the two writes execute as a single Redis script, so there is no
 * read-modify-write race even under concurrent updaters.
 */
@Slf4j
@Service
public class DroneStateService {

    private static final String KEY_PREFIX = "drone:state:";
    private static final String VER_PREFIX = "drone:ver:";

    /**
     * KEYS[1]=state key, KEYS[2]=version key; ARGV[1]=version (epoch millis),
     * ARGV[2]=state JSON, ARGV[3]=TTL millis. Writes only if newer-or-equal.
     */
    private static final RedisScript<Long> CAS_SCRIPT = new DefaultRedisScript<>(
            "local cur = tonumber(redis.call('GET', KEYS[2]))\n"
            + "local ver = tonumber(ARGV[1])\n"
            + "if cur == nil or ver >= cur then\n"
            + "  redis.call('SET', KEYS[1], ARGV[2], 'PX', ARGV[3])\n"
            + "  redis.call('SET', KEYS[2], ARGV[1], 'PX', ARGV[3])\n"
            + "  return 1\n"
            + "end\n"
            + "return 0",
            Long.class);

    private final StringRedisTemplate redis;
    private final ObjectMapper objectMapper;
    private final MessageBroker messageBroker;
    private final Duration ttl;

    public DroneStateService(StringRedisTemplate redis,
                             ObjectMapper objectMapper,
                             MessageBroker messageBroker,
                             @Value("${app.state.ttl-seconds:30}") long ttlSeconds) {
        this.redis = redis;
        this.objectMapper = objectMapper;
        this.messageBroker = messageBroker;
        this.ttl = Duration.ofSeconds(ttlSeconds);
    }

    /** Subscribe to the telemetry stream so the cache stays current. */
    @PostConstruct
    void subscribe() {
        messageBroker.subscribe(BrokerChannels.TELEMETRY, TelemetryMessage.class, this::update);
    }

    /**
     * Atomically advance the latest-state snapshot for a drone, refreshing its
     * TTL. Older (out-of-order) samples are ignored.
     */
    public void update(TelemetryMessage telemetry) {
        try {
            DroneState state = DroneState.from(telemetry);
            long version = telemetry.timestamp().toEpochMilli();
            redis.execute(CAS_SCRIPT,
                    List.of(key(telemetry.droneId()), versionKey(telemetry.droneId())),
                    Long.toString(version),
                    objectMapper.writeValueAsString(state),
                    Long.toString(ttl.toMillis()));
        } catch (Exception e) {
            log.error("Failed to cache state for drone {}: {}",
                    telemetry.droneId(), e.getMessage());
        }
    }

    public Optional<DroneState> getState(String droneId) {
        String json = redis.opsForValue().get(key(droneId));
        return Optional.ofNullable(json).map(this::deserialize);
    }

    /** Snapshot of every drone currently considered online (non-expired). */
    public List<DroneState> getAllStates() {
        Set<String> keys = redis.keys(KEY_PREFIX + "*");
        if (keys == null || keys.isEmpty()) {
            return Collections.emptyList();
        }
        List<String> values = redis.opsForValue().multiGet(keys);
        List<DroneState> states = new ArrayList<>();
        if (values != null) {
            for (String json : values) {
                if (json != null) {
                    states.add(deserialize(json));
                }
            }
        }
        return states;
    }

    private DroneState deserialize(String json) {
        try {
            return objectMapper.readValue(json, DroneState.class);
        } catch (Exception e) {
            throw new IllegalStateException("Corrupt drone state in cache", e);
        }
    }

    private String key(String droneId) {
        return KEY_PREFIX + droneId;
    }

    private String versionKey(String droneId) {
        return VER_PREFIX + droneId;
    }
}
