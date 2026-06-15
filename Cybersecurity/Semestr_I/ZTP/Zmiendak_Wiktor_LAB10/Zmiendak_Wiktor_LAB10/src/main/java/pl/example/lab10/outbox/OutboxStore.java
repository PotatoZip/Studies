package pl.example.lab10.outbox;

import org.springframework.stereotype.Component;
import pl.example.lab10.events.DomainEvent;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class OutboxStore {

  private final AtomicLong sequence = new AtomicLong(1);
  private final List<OutboxEvent> events = new CopyOnWriteArrayList<>();

  public OutboxEvent save(String routingKey, DomainEvent payload, Instant createdAt) {
    if (routingKey == null || routingKey.isBlank()) {
      throw new IllegalArgumentException("Routing key must not be blank");
    }
    if (payload == null) {
      throw new IllegalArgumentException("Payload must not be null");
    }

    OutboxEvent event = new OutboxEvent(sequence.getAndIncrement(), routingKey, payload, createdAt);
    events.add(event);
    return event;
  }

  public List<OutboxEvent> findUnprocessed() {
    return events.stream()
        .filter(event -> !event.isProcessed())
        .sorted(Comparator.comparingLong(OutboxEvent::getId))
        .toList();
  }

  public List<OutboxEvent> findAll() {
    return new ArrayList<>(events).stream()
        .sorted(Comparator.comparingLong(OutboxEvent::getId))
        .toList();
  }
}
