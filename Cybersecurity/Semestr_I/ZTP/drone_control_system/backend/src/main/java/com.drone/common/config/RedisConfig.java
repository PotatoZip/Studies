package com.drone.common.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * Redis wiring for two responsibilities:
 * <ul>
 *   <li>the "Latest State" cache — a {@link RedisTemplate} with String keys and
 *       JSON values (see {@code DroneStateService});</li>
 *   <li>Pub/Sub messaging — a shared {@link RedisMessageListenerContainer} used
 *       by {@code RedisMessageBroker} to register channel listeners.</li>
 * </ul>
 *
 * {@code StringRedisTemplate} (used for publishing JSON strings) is
 * auto-configured by Spring Boot, so only the object template and the listener
 * container need to be declared here.
 */
@Configuration
public class RedisConfig {

    /**
     * Template for storing JSON-serialized objects (latest drone state) under
     * String keys with per-key TTLs.
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        StringRedisSerializer keySerializer = new StringRedisSerializer();
        GenericJackson2JsonRedisSerializer valueSerializer =
                new GenericJackson2JsonRedisSerializer();

        template.setKeySerializer(keySerializer);
        template.setHashKeySerializer(keySerializer);
        template.setValueSerializer(valueSerializer);
        template.setHashValueSerializer(valueSerializer);
        template.afterPropertiesSet();
        return template;
    }

    /**
     * Shared listener container backing the Pub/Sub message broker. It manages
     * its own thread pool and dispatches to every registered listener.
     */
    @Bean
    public RedisMessageListenerContainer redisMessageListenerContainer(
            RedisConnectionFactory connectionFactory) {
        RedisMessageListenerContainer container = new RedisMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);
        return container;
    }
}
