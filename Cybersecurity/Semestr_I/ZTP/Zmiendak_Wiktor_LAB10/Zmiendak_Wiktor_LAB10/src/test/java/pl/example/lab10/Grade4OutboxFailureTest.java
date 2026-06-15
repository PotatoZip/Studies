package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.broker.MessageBroker;
import pl.example.lab10.events.DomainEvent;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.outbox.OutboxEvent;
import pl.example.lab10.outbox.OutboxProcessor;
import pl.example.lab10.outbox.OutboxStore;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

class Grade4OutboxFailureTest {

  private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T10:15:30Z"), ZoneOffset.UTC);

  @Test
  @DisplayName("Jeżeli broker rzuci wyjątek, event nie zostaje oznaczony jako processed")
  void failedPublishDoesNotMarkOutboxEventAsProcessed() {
    OutboxStore outboxStore = new OutboxStore();
    OutboxEvent outboxEvent = outboxStore.save(
        "orders.created",
        new OrderCreatedEvent("event-1", clock.instant(), 1L, 10L, 2),
        clock.instant()
    );

    MessageBroker failingBroker = new MessageBroker() {
      @Override
      public void subscribe(String routingKey, Consumer<DomainEvent> handler) {
      }

      @Override
      public void publish(String routingKey, DomainEvent event) {
        throw new RuntimeException("Broker is down");
      }
    };

    OutboxProcessor processor = new OutboxProcessor(outboxStore, failingBroker, clock);

    RuntimeException exception = assertThrows(RuntimeException.class, processor::processPending);

    assertEquals("Broker is down", exception.getMessage());
    assertNull(outboxEvent.getProcessedAt());
  }
}
