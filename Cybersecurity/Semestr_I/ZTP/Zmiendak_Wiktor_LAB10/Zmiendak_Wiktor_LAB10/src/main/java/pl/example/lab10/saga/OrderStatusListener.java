package pl.example.lab10.saga;

import org.springframework.stereotype.Component;
import pl.example.lab10.events.StockReservationFailedEvent;
import pl.example.lab10.events.StockReservedEvent;
import pl.example.lab10.order.OrderStore;

@Component
public class OrderStatusListener {

  private final OrderStore orderStore;
  private final ProcessedEventsStore processedEventsStore;

  public OrderStatusListener(OrderStore orderStore, ProcessedEventsStore processedEventsStore) {
    this.orderStore = orderStore;
    this.processedEventsStore = processedEventsStore;
  }

  public void handle(StockReservedEvent event) {
    if (!processedEventsStore.tryMarkProcessed(event.eventId())) {
      return;
    }
    orderStore.confirm(event.orderId());
  }

  public void handle(StockReservationFailedEvent event) {
    if (!processedEventsStore.tryMarkProcessed(event.eventId())) {
      return;
    }
    orderStore.reject(event.orderId(), event.reason());
  }
}
