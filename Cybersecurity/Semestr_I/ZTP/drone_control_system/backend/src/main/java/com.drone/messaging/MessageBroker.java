package com.drone.messaging;

import java.util.function.Consumer;

/**
 * Abstraction over the pub/sub message broker that decouples the GCS backend
 * from the underlying transport. The default implementation
 * ({@code RedisMessageBroker}) uses Redis Pub/Sub; an MQTT-backed
 * implementation could be dropped in without touching callers.
 *
 * <p>Payloads are serialized to JSON on publish and deserialized into the
 * requested type on delivery.
 */
public interface MessageBroker {

    /**
     * Publish a payload to the given channel. The payload is serialized to JSON.
     */
    void publish(String channel, Object payload);

    /**
     * Register a typed handler for every message delivered on the channel.
     * Handlers are invoked on broker listener threads, so they must be
     * thread-safe and non-blocking.
     *
     * @param channel the channel to subscribe to
     * @param type    target type the JSON payload is deserialized into
     * @param handler callback receiving each deserialized message
     */
    <T> void subscribe(String channel, Class<T> type, Consumer<T> handler);
}
