package pl.example.lab5.broker;

import java.util.function.Consumer;

public interface MessageBroker {
  void subscribe(String routingKey, Consumer<Object> handler);
  void publish(String routingKey, Object message);
}
