package pl.example.lab5.broker;

import org.springframework.stereotype.Component;

import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;

@Component
public class InMemoryMessageBroker implements MessageBroker {

  private final Map<String, List<Consumer<Object>>> subscribers = new ConcurrentHashMap<>();

  // Daemon threads so unit tests don't hang the JVM after execution.
  private final Executor executor = Executors.newCachedThreadPool(r -> {
    Thread t = new Thread(r);
    t.setDaemon(true);
    t.setName("broker-" + t.getId());
    return t;
  });

  @Override
  public void subscribe(String routingKey, Consumer<Object> handler) {
    subscribers.computeIfAbsent(routingKey, rk -> new CopyOnWriteArrayList<>()).add(handler);
  }

  @Override
  public void publish(String routingKey, Object message) {
    List<Consumer<Object>> handlers = subscribers.get(routingKey);
    if (handlers == null || handlers.isEmpty()) {
      return;
    }

    for (Consumer<Object> handler : handlers) {
      executor.execute(() -> handler.accept(message));
    }
  }
}
