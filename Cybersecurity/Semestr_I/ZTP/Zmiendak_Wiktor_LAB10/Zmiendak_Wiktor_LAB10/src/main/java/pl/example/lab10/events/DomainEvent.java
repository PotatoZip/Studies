package pl.example.lab10.events;

import java.time.Instant;

public interface DomainEvent {

  String eventId();

  Instant occurredAt();
}
