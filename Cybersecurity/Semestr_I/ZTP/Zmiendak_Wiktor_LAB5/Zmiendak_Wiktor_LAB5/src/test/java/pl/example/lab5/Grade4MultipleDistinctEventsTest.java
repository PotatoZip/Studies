package pl.example.lab5;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import pl.example.lab5.broker.MessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.store.ReceivedEventsStore;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
class Grade4MultipleDistinctEventsTest {

  @Autowired MessageBroker broker;
  @Autowired ReceivedEventsStore store;

  @BeforeEach
  void setup() {
    store.clear();
  }

  @Test
  @DisplayName("4.0: Dwa eventy z różnymi eventId są zapisane jako dwa wpisy")
  void shouldStoreTwoDifferentEvents() throws Exception {
    broker.publish("orders.created", new OrderCreatedEvent("e1", 1, 1, 1, 120.0));
    broker.publish("orders.created", new OrderCreatedEvent("e2", 2, 2, 2, 160.0));

    assertTrue(waitUntil(() -> store.size() == 2, 1000), "Expected 2 events");
    assertEquals(2, store.size());
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
