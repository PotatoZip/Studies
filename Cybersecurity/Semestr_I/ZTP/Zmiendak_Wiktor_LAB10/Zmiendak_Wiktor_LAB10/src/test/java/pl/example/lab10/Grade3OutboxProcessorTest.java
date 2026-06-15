package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.broker.InMemoryMessageBroker;
import pl.example.lab10.events.DomainEvent;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.outbox.OutboxEvent;
import pl.example.lab10.outbox.OutboxProcessor;
import pl.example.lab10.outbox.OutboxStore;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;

class Grade3OutboxProcessorTest {

  private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T10:15:30Z"), ZoneOffset.UTC);

  @Test
  @DisplayName("OutboxProcessor publikuje nieprzetworzony event i oznacza go jako processed")
  void processPendingPublishesAndMarksEvent() {
    OutboxStore outboxStore = new OutboxStore();
    InMemoryMessageBroker broker = new InMemoryMessageBroker();
    OutboxProcessor processor = new OutboxProcessor(outboxStore, broker, clock);

    OrderCreatedEvent payload = new OrderCreatedEvent("event-1", clock.instant(), 1L, 10L, 2);
    OutboxEvent outboxEvent = outboxStore.save("orders.created", payload, clock.instant());

    AtomicReference<DomainEvent> received = new AtomicReference<>();
    broker.subscribe("orders.created", received::set);

    int processed = processor.processPending();

    assertEquals(1, processed);
    assertSame(payload, received.get());
    assertNotNull(outboxEvent.getProcessedAt());
    assertEquals(clock.instant(), outboxEvent.getProcessedAt());

    assertEquals(0, processor.processPending());
  }
}
