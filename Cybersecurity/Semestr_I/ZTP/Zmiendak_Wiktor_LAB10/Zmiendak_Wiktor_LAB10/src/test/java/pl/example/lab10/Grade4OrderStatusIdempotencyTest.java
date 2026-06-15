package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.events.StockReservationFailedEvent;
import pl.example.lab10.order.Order;
import pl.example.lab10.order.OrderStatus;
import pl.example.lab10.order.OrderStore;
import pl.example.lab10.saga.OrderStatusListener;
import pl.example.lab10.saga.ProcessedEventsStore;

import java.time.Instant;

import static org.junit.jupiter.api.Assertions.assertEquals;

class Grade4OrderStatusIdempotencyTest {

  @Test
  @DisplayName("Duplikat eventu wyniku nie nadpisuje powodu odrzucenia")
  void duplicateFailureEventDoesNotOverwriteOrderAgain() {
    OrderStore orderStore = new OrderStore();
    Order order = orderStore.create(10L, 9, Instant.parse("2026-01-01T10:15:30Z"));
    ProcessedEventsStore processedEventsStore = new ProcessedEventsStore();
    OrderStatusListener listener = new OrderStatusListener(orderStore, processedEventsStore);

    listener.handle(new StockReservationFailedEvent(
        "same-stock-event",
        Instant.parse("2026-01-01T10:16:00Z"),
        order.getId(),
        10L,
        9,
        "Insufficient stock"
    ));

    listener.handle(new StockReservationFailedEvent(
        "same-stock-event",
        Instant.parse("2026-01-01T10:17:00Z"),
        order.getId(),
        10L,
        9,
        "Other reason that must not overwrite state"
    ));

    Order saved = orderStore.findById(order.getId()).orElseThrow();
    assertEquals(OrderStatus.REJECTED, saved.getStatus());
    assertEquals("Insufficient stock", saved.getRejectionReason());
    assertEquals(1, processedEventsStore.count());
  }
}
