package pl.example.lab5.service;

import org.springframework.stereotype.Component;
import pl.example.lab5.broker.MessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;

@Component
public class OrderEventPublisher {

  private final MessageBroker broker;

  public OrderEventPublisher(MessageBroker broker) {
    this.broker = broker;
  }

  public void publishOrderCreated(OrderCreatedEvent event) {
    broker.publish("orders.created", event);
  }
}
