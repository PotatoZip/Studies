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

@SpringBootTest
class Grade4NullEventIdIgnoredTest {

  @Autowired MessageBroker broker;
  @Autowired ReceivedEventsStore store;

  @BeforeEach
  void setup() {
    store.clear();
  }

  @Test
  @DisplayName("4.0: Event bez eventId jest ignorowany (nie psuje idempotencji)")
  void shouldIgnoreNullEventId() throws Exception {
    broker.publish("orders.created", new OrderCreatedEvent(null, 1, 1, 1, 120.0));

    // krótka chwila na asynchroniczne dostarczenie
    Thread.sleep(150);
    assertEquals(0, store.size());
  }
}
