package pl.example.lab5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab5.broker.MessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.service.OrderEventPublisher;

import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.*;

class Grade3PublisherRoutingKeyTest {

  @Test
  @DisplayName("3.0: Publisher publikuje OrderCreatedEvent na routingKey orders.created")
  void publisherShouldUseOrdersCreatedRoutingKey() {
    AtomicReference<String> rk = new AtomicReference<>();
    AtomicReference<Object> msg = new AtomicReference<>();

    MessageBroker recordingBroker = new MessageBroker() {
      @Override public void subscribe(String routingKey, Consumer<Object> handler) { /* no-op */ }
      @Override public void publish(String routingKey, Object message) {
        rk.set(routingKey);
        msg.set(message);
      }
    };

    OrderEventPublisher publisher = new OrderEventPublisher(recordingBroker);
    OrderCreatedEvent e = new OrderCreatedEvent("evt-1", 10L, 1L, 2, 240.0);

    publisher.publishOrderCreated(e);

    assertEquals("orders.created", rk.get());
    assertSame(e, msg.get(), "Publisher should publish the same event instance");
  }
}
