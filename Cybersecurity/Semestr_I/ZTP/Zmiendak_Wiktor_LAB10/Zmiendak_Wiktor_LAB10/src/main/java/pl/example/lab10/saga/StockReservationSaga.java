package pl.example.lab10.saga;

import org.springframework.stereotype.Component;
import pl.example.lab10.broker.MessageBroker;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.product.ProductCatalog;

import java.time.Clock;
import java.time.Instant;
import java.util.UUID;
import pl.example.lab10.events.StockReservedEvent;
import pl.example.lab10.events.StockReservationFailedEvent;
import pl.example.lab10.product.InsufficientStockException;
import pl.example.lab10.product.ProductNotFoundException;

@Component
public class StockReservationSaga {

  private final ProductCatalog productCatalog;
  private final MessageBroker messageBroker;
  private final ProcessedEventsStore processedEventsStore;
  private final Clock clock;

  public StockReservationSaga(
      ProductCatalog productCatalog,
      MessageBroker messageBroker,
      ProcessedEventsStore processedEventsStore,
      Clock clock) {
    this.productCatalog = productCatalog;
    this.messageBroker = messageBroker;
    this.processedEventsStore = processedEventsStore;
    this.clock = clock;
  }

  public void handle(OrderCreatedEvent event) {
    if (!processedEventsStore.tryMarkProcessed(event.eventId())) {
      return;
    }

    try {
      productCatalog.reserve(event.productId(), event.quantity());
      StockReservedEvent reserved = new StockReservedEvent(
          UUID.randomUUID().toString(),
          Instant.now(clock),
          event.orderId(),
          event.productId(),
          event.quantity());
      messageBroker.publish("stock.reserved", reserved);
    } catch (ProductNotFoundException | InsufficientStockException e) {
      StockReservationFailedEvent failed = new StockReservationFailedEvent(
          UUID.randomUUID().toString(),
          Instant.now(clock),
          event.orderId(),
          event.productId(),
          event.quantity(),
          e.getMessage());
      messageBroker.publish("stock.reservation.failed", failed);
    }
  }
}
