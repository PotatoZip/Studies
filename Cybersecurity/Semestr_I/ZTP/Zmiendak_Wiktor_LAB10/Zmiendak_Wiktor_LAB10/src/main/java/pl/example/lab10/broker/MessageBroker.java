package pl.example.lab10.broker;

import pl.example.lab10.events.DomainEvent;

import java.util.function.Consumer;

public interface MessageBroker {

  void subscribe(String routingKey, Consumer<DomainEvent> handler);

  void publish(String routingKey, DomainEvent event);
}
