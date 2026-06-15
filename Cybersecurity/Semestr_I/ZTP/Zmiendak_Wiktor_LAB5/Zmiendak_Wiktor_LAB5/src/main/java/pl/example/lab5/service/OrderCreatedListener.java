package pl.example.lab5.service;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import pl.example.lab5.broker.MessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.store.ReceivedEventsStore;

@Component
public class OrderCreatedListener {

  private final MessageBroker broker;
  private final ReceivedEventsStore store;

  public OrderCreatedListener(MessageBroker broker, ReceivedEventsStore store) {
    this.broker = broker;
    this.store = store;
  }

  @PostConstruct
  public void init() {
    broker.subscribe("orders.created", message -> {
      if (message instanceof OrderCreatedEvent event) {
        store.addIfFirstTime(event);
      }
    });
  }
}
