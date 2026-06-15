package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.order.Order;
import pl.example.lab10.order.OrderServiceImpl;
import pl.example.lab10.order.OrderStatus;
import pl.example.lab10.order.OrderStore;
import pl.example.lab10.outbox.OutboxEvent;
import pl.example.lab10.outbox.OutboxStore;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class Grade3OrderCreatesOutboxEventTest {

  private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T10:15:30Z"), ZoneOffset.UTC);

  @Test
  @DisplayName("Utworzenie zamówienia zapisuje OrderCreatedEvent w outboxie")
  void createOrderStoresOrderCreatedEventInOutbox() {
    OrderStore orderStore = new OrderStore();
    OutboxStore outboxStore = new OutboxStore();
    OrderServiceImpl service = new OrderServiceImpl(orderStore, outboxStore, clock);

    Order order = service.createOrder(77L, 3);

    assertEquals(1L, order.getId());
    assertEquals(77L, order.getProductId());
    assertEquals(3, order.getQuantity());
    assertEquals(OrderStatus.PENDING, order.getStatus());

    List<OutboxEvent> events = outboxStore.findAll();
    assertEquals(1, events.size());

    OutboxEvent outboxEvent = events.get(0);
    assertEquals("orders.created", outboxEvent.getRoutingKey());
    assertFalse(outboxEvent.isProcessed());
    assertNull(outboxEvent.getProcessedAt());
    assertEquals(clock.instant(), outboxEvent.getCreatedAt());

    assertInstanceOf(OrderCreatedEvent.class, outboxEvent.getPayload());
    OrderCreatedEvent payload = (OrderCreatedEvent) outboxEvent.getPayload();
    assertNotNull(payload.eventId());
    assertFalse(payload.eventId().isBlank());
    assertEquals(clock.instant(), payload.occurredAt());
    assertEquals(order.getId(), payload.orderId());
    assertEquals(77L, payload.productId());
    assertEquals(3, payload.quantity());
  }

  @Test
  @DisplayName("Zamówienie z quantity <= 0 jest odrzucane i nie zapisuje eventu")
  void invalidQuantityDoesNotCreateOutboxEvent() {
    OrderStore orderStore = new OrderStore();
    OutboxStore outboxStore = new OutboxStore();
    OrderServiceImpl service = new OrderServiceImpl(orderStore, outboxStore, clock);

    try {
      service.createOrder(77L, 0);
    } catch (IllegalArgumentException expected) {
      // oczekiwane zachowanie
    }

    assertEquals(0, orderStore.findAll().size());
    assertEquals(0, outboxStore.findAll().size());
  }
}
