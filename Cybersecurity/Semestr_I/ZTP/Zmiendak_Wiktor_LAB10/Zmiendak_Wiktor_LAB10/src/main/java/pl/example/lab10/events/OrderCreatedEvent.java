package pl.example.lab10.events;

import java.time.Instant;

public record OrderCreatedEvent(
    String eventId,
    Instant occurredAt,
    long orderId,
    long productId,
    int quantity
) implements DomainEvent {
}
