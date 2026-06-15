package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.events.StockReservationFailedEvent;
import pl.example.lab10.events.StockReservedEvent;
import pl.example.lab10.order.Order;
import pl.example.lab10.order.OrderStatus;
import pl.example.lab10.order.OrderStore;
import pl.example.lab10.saga.OrderStatusListener;
import pl.example.lab10.saga.ProcessedEventsStore;

import java.time.Instant;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

class Grade3OrderStatusListenerTest {

  @Test
  @DisplayName("StockReservedEvent potwierdza zamówienie")
  void stockReservedConfirmsOrder() {
    OrderStore orderStore = new OrderStore();
    Order order = orderStore.create(10L, 2, Instant.parse("2026-01-01T10:15:30Z"));
    OrderStatusListener listener = new OrderStatusListener(orderStore, new ProcessedEventsStore());

    listener.handle(new StockReservedEvent("stock-event-1", Instant.parse("2026-01-01T10:16:00Z"), order.getId(), 10L, 2));

    Order saved = orderStore.findById(order.getId()).orElseThrow();
    assertEquals(OrderStatus.CONFIRMED, saved.getStatus());
    assertNull(saved.getRejectionReason());
  }

  @Test
  @DisplayName("StockReservationFailedEvent odrzuca zamówienie z powodem")
  void stockReservationFailedRejectsOrder() {
    OrderStore orderStore = new OrderStore();
    Order order = orderStore.create(10L, 9, Instant.parse("2026-01-01T10:15:30Z"));
    OrderStatusListener listener = new OrderStatusListener(orderStore, new ProcessedEventsStore());

    listener.handle(new StockReservationFailedEvent(
        "stock-event-2",
        Instant.parse("2026-01-01T10:16:00Z"),
        order.getId(),
        10L,
        9,
        "Insufficient stock"
    ));

    Order saved = orderStore.findById(order.getId()).orElseThrow();
    assertEquals(OrderStatus.REJECTED, saved.getStatus());
    assertEquals("Insufficient stock", saved.getRejectionReason());
  }
}
