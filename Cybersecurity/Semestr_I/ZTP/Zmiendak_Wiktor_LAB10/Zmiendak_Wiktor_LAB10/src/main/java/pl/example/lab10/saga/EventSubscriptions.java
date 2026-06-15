package pl.example.lab10.saga;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import pl.example.lab10.broker.MessageBroker;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.events.StockReservationFailedEvent;
import pl.example.lab10.events.StockReservedEvent;

@Component
public class EventSubscriptions {

  private final MessageBroker messageBroker;
  private final StockReservationSaga stockReservationSaga;
  private final OrderStatusListener orderStatusListener;

  public EventSubscriptions(
      MessageBroker messageBroker,
      StockReservationSaga stockReservationSaga,
      OrderStatusListener orderStatusListener
  ) {
    this.messageBroker = messageBroker;
    this.stockReservationSaga = stockReservationSaga;
    this.orderStatusListener = orderStatusListener;
  }

  @PostConstruct
  public void subscribe() {
    messageBroker.subscribe("orders.created", event -> stockReservationSaga.handle((OrderCreatedEvent) event));
    messageBroker.subscribe("stock.reserved", event -> orderStatusListener.handle((StockReservedEvent) event));
    messageBroker.subscribe("stock.reservation.failed", event -> orderStatusListener.handle((StockReservationFailedEvent) event));
  }
}
