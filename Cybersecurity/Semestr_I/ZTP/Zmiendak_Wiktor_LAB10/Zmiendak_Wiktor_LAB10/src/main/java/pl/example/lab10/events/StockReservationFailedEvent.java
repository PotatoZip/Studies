package pl.example.lab10.events;

import java.time.Instant;

public record StockReservationFailedEvent(
    String eventId,
    Instant occurredAt,
    long orderId,
    long productId,
    int quantity,
    String reason
) implements DomainEvent {
}
