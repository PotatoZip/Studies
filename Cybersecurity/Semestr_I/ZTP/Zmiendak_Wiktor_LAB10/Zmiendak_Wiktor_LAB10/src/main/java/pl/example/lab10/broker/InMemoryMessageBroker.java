package pl.example.lab10.broker;

import org.springframework.stereotype.Component;
import pl.example.lab10.events.DomainEvent;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

@Component
public class InMemoryMessageBroker implements MessageBroker {

  private final Map<String, List<Consumer<DomainEvent>>> subscribers = new ConcurrentHashMap<>();

  @Override
  public void subscribe(String routingKey, Consumer<DomainEvent> handler) {
    subscribers.computeIfAbsent(routingKey, ignored -> new CopyOnWriteArrayList<>()).add(handler);
  }

  @Override
  public void publish(String routingKey, DomainEvent event) {
    subscribers.getOrDefault(routingKey, List.of()).forEach(handler -> handler.accept(event));
  }
}
