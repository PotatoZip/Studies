package com.drone.messaging.redis;

import com.drone.messaging.MessageBroker;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.charset.StandardCharsets;
import java.util.function.Consumer;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.listener.ChannelTopic;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;
import org.springframework.stereotype.Component;

/**
 * Redis Pub/Sub implementation of {@link MessageBroker}.
 *
 * <p>Messages are published as JSON strings via {@link StringRedisTemplate} and
 * delivered through a shared {@link RedisMessageListenerContainer}. Each
 * {@link #subscribe} call registers an independent listener, so multiple
 * subscribers can consume the same channel (e.g. telemetry is consumed by the
 * WebSocket broadcaster, the state cache, and the persistence buffer).
 */
@Slf4j
@Component
public class RedisMessageBroker implements MessageBroker {

    private final StringRedisTemplate redisTemplate;
    private final RedisMessageListenerContainer listenerContainer;
    private final ObjectMapper objectMapper;

    public RedisMessageBroker(StringRedisTemplate redisTemplate,
                              RedisMessageListenerContainer listenerContainer,
                              ObjectMapper objectMapper) {
        this.redisTemplate = redisTemplate;
        this.listenerContainer = listenerContainer;
        this.objectMapper = objectMapper;
    }

    @Override
    public void publish(String channel, Object payload) {
        try {
            String json = objectMapper.writeValueAsString(payload);
            redisTemplate.convertAndSend(channel, json);
        } catch (Exception e) {
            log.error("Failed to publish to channel '{}': {}", channel, e.getMessage());
        }
    }

    @Override
    public <T> void subscribe(String channel, Class<T> type, Consumer<T> handler) {
        MessageListener listener = (message, pattern) -> {
            String body = new String(message.getBody(), StandardCharsets.UTF_8);
            try {
                handler.accept(objectMapper.readValue(body, type));
            } catch (Exception e) {
                log.error("Failed to handle message on '{}': {}", channel, e.getMessage());
            }
        };
        listenerContainer.addMessageListener(listener, new ChannelTopic(channel));
        log.info("Subscribed to broker channel '{}' -> {}", channel, type.getSimpleName());
    }
}
