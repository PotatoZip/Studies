package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.broker.InMemoryMessageBroker;
import pl.example.lab10.events.DomainEvent;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.events.StockReservationFailedEvent;
import pl.example.lab10.events.StockReservedEvent;
import pl.example.lab10.product.Product;
import pl.example.lab10.product.ProductCatalog;
import pl.example.lab10.saga.ProcessedEventsStore;
import pl.example.lab10.saga.StockReservationSaga;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class Grade3StockReservationSagaTest {

  private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T10:15:30Z"), ZoneOffset.UTC);

  @Test
  @DisplayName("Saga rezerwuje produkt i publikuje StockReservedEvent")
  void sagaReservesStockAndPublishesSuccessEvent() {
    ProductCatalog catalog = new ProductCatalog();
    Product product = catalog.create("Keyboard", 5);
    InMemoryMessageBroker broker = new InMemoryMessageBroker();
    StockReservationSaga saga = new StockReservationSaga(catalog, broker, new ProcessedEventsStore(), clock);

    List<DomainEvent> published = new ArrayList<>();
    broker.subscribe("stock.reserved", published::add);

    saga.handle(new OrderCreatedEvent("order-event-1", clock.instant(), 100L, product.getId(), 2));

    assertEquals(3, catalog.findById(product.getId()).orElseThrow().getStock());
    assertEquals(1, published.size());
    assertInstanceOf(StockReservedEvent.class, published.get(0));

    StockReservedEvent event = (StockReservedEvent) published.get(0);
    assertNotNull(event.eventId());
    assertFalse(event.eventId().isBlank());
    assertEquals(clock.instant(), event.occurredAt());
    assertEquals(100L, event.orderId());
    assertEquals(product.getId(), event.productId());
    assertEquals(2, event.quantity());
  }

  @Test
  @DisplayName("Saga publikuje StockReservationFailedEvent, gdy nie ma wystarczającego stocku")
  void sagaPublishesFailureWhenStockIsInsufficient() {
    ProductCatalog catalog = new ProductCatalog();
    Product product = catalog.create("Mouse", 1);
    InMemoryMessageBroker broker = new InMemoryMessageBroker();
    StockReservationSaga saga = new StockReservationSaga(catalog, broker, new ProcessedEventsStore(), clock);

    List<DomainEvent> published = new ArrayList<>();
    broker.subscribe("stock.reservation.failed", published::add);

    saga.handle(new OrderCreatedEvent("order-event-2", clock.instant(), 200L, product.getId(), 5));

    assertEquals(1, catalog.findById(product.getId()).orElseThrow().getStock());
    assertEquals(1, published.size());
    assertInstanceOf(StockReservationFailedEvent.class, published.get(0));

    StockReservationFailedEvent event = (StockReservationFailedEvent) published.get(0);
    assertNotNull(event.eventId());
    assertFalse(event.eventId().isBlank());
    assertEquals(clock.instant(), event.occurredAt());
    assertEquals(200L, event.orderId());
    assertEquals(product.getId(), event.productId());
    assertEquals(5, event.quantity());
    assertEquals("Insufficient stock", event.reason());
  }
}
