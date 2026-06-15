package pl.example.lab5;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import pl.example.lab5.broker.MessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.store.ReceivedEventsStore;

import java.util.stream.IntStream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class Grade4ConcurrentDuplicateDeliveryTest {

  @Autowired MessageBroker broker;
  @Autowired ReceivedEventsStore store;

  @BeforeEach
  void setup() {
    store.clear();
  }

  @Test
  @DisplayName("4.0: Duplikaty tego samego eventu (równolegle) nie zwiększają liczby zapisów")
  void concurrentDuplicatesShouldStillResultInSingleStoredEvent() throws Exception {
    OrderCreatedEvent e = new OrderCreatedEvent("dup-1", 1, 1, 1, 120.0);

    IntStream.range(0, 25).parallel().forEach(i -> broker.publish("orders.created", e));

    assertTrue(waitUntil(() -> store.size() == 1, 1000), "Expected exactly 1 stored event");
    assertEquals(1, store.size());
  }

  private boolean waitUntil(Check c, long timeoutMs) throws InterruptedException {
    long start = System.currentTimeMillis();
    while (System.currentTimeMillis() - start < timeoutMs) {
      if (c.ok()) return true;
      Thread.sleep(20);
    }
    return false;
  }

  @FunctionalInterface
  interface Check { boolean ok(); }
}
