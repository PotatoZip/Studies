package pl.example.lab5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab5.broker.InMemoryMessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.service.OrderCreatedListener;
import pl.example.lab5.store.ReceivedEventsStore;

import static org.junit.jupiter.api.Assertions.*;

class Grade3ListenerConsumesEventTest {

  @Test
  @DisplayName("3.0: Listener subskrybuje orders.created i zapisuje event w store")
  void listenerShouldSubscribeAndStore() throws Exception {
    InMemoryMessageBroker broker = new InMemoryMessageBroker();
    ReceivedEventsStore store = new ReceivedEventsStore();
    OrderCreatedListener listener = new OrderCreatedListener(broker, store);

    listener.init();

    OrderCreatedEvent e = new OrderCreatedEvent("evt-123", 1L, 2L, 3, 240.0);
    broker.publish("orders.created", e);

    assertTrue(waitUntil(() -> store.size() == 1, 1000), "Expected event to be stored");
    assertEquals("evt-123", store.getEvents().get(0).getEventId());
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
