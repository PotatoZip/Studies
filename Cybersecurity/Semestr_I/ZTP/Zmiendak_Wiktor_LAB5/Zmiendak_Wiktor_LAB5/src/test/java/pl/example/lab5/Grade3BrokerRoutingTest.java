package pl.example.lab5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab5.broker.InMemoryMessageBroker;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

class Grade3BrokerRoutingTest {

  @Test
  @DisplayName("3.0: Broker routuje wiadomości tylko do subskrybentów danego routingKey")
  void shouldRouteOnlyToMatchingRoutingKey() throws Exception {
    InMemoryMessageBroker broker = new InMemoryMessageBroker();

    AtomicInteger a = new AtomicInteger();
    AtomicInteger b = new AtomicInteger();
    CountDownLatch latch = new CountDownLatch(1);

    broker.subscribe("rk.a", msg -> {
      a.incrementAndGet();
      latch.countDown();
    });
    broker.subscribe("rk.b", msg -> b.incrementAndGet());

    broker.publish("rk.a", "hello");

    assertTrue(latch.await(500, TimeUnit.MILLISECONDS), "Expected handler for rk.a to be invoked");
    assertEquals(1, a.get());
    assertEquals(0, b.get());
  }

  @Test
  @DisplayName("3.0: Broker robi fan-out do wielu subskrybentów pod tym samym routingKey")
  void shouldFanOutToMultipleSubscribers() throws Exception {
    InMemoryMessageBroker broker = new InMemoryMessageBroker();

    CountDownLatch latch = new CountDownLatch(2);
    broker.subscribe("rk", msg -> latch.countDown());
    broker.subscribe("rk", msg -> latch.countDown());

    broker.publish("rk", 123);

    assertTrue(latch.await(500, TimeUnit.MILLISECONDS), "Expected both subscribers to be invoked");
  }

  @Test
  @DisplayName("3.0: Publikacja na routingKey bez subskrybentów nie rzuca wyjątku")
  void publishWithNoSubscribersShouldNotThrow() {
    InMemoryMessageBroker broker = new InMemoryMessageBroker();
    assertDoesNotThrow(() -> broker.publish("no.listeners", "msg"));
  }
}
