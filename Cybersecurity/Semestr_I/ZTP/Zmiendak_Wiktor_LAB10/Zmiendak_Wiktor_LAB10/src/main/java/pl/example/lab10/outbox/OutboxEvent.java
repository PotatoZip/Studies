package pl.example.lab10.outbox;

import pl.example.lab10.events.DomainEvent;

import java.time.Instant;

public class OutboxEvent {

  private final long id;
  private final String routingKey;
  private final DomainEvent payload;
  private final Instant createdAt;
  private Instant processedAt;

  public OutboxEvent(long id, String routingKey, DomainEvent payload, Instant createdAt) {
    this.id = id;
    this.routingKey = routingKey;
    this.payload = payload;
    this.createdAt = createdAt;
  }

  public long getId() {
    return id;
  }

  public String getRoutingKey() {
    return routingKey;
  }

  public DomainEvent getPayload() {
    return payload;
  }

  public Instant getCreatedAt() {
    return createdAt;
  }

  public Instant getProcessedAt() {
    return processedAt;
  }

  public boolean isProcessed() {
    return processedAt != null;
  }

  public void markProcessed(Instant processedAt) {
    this.processedAt = processedAt;
  }
}
