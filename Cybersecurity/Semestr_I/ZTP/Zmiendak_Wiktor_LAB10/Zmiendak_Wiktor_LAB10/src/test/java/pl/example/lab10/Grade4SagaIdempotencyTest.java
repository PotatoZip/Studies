package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.broker.InMemoryMessageBroker;
import pl.example.lab10.events.DomainEvent;
import pl.example.lab10.events.OrderCreatedEvent;
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

class Grade4SagaIdempotencyTest {

  private final Clock clock = Clock.fixed(Instant.parse("2026-01-01T10:15:30Z"), ZoneOffset.UTC);

  @Test
  @DisplayName("Duplikat OrderCreatedEvent nie rezerwuje stocku drugi raz")
  void duplicateOrderCreatedEventIsIgnoredBySaga() {
    ProductCatalog catalog = new ProductCatalog();
    Product product = catalog.create("Monitor", 5);
    InMemoryMessageBroker broker = new InMemoryMessageBroker();
    ProcessedEventsStore processedEventsStore = new ProcessedEventsStore();
    StockReservationSaga saga = new StockReservationSaga(catalog, broker, processedEventsStore, clock);

    List<DomainEvent> published = new ArrayList<>();
    broker.subscribe("stock.reserved", published::add);

    OrderCreatedEvent event = new OrderCreatedEvent("same-order-event", clock.instant(), 100L, product.getId(), 2);

    saga.handle(event);
    saga.handle(event);

    assertEquals(3, catalog.findById(product.getId()).orElseThrow().getStock());
    assertEquals(1, published.size());
    assertEquals(1, processedEventsStore.count());
  }
}
