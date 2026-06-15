package pl.example.lab5;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import pl.example.lab5.broker.MessageBroker;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.store.ReceivedEventsStore;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class Grade4IdempotencyTest {

  @Autowired MockMvc mockMvc;
  @Autowired ReceivedEventsStore store;
  @Autowired MessageBroker broker;

  @BeforeEach
  void setup() {
    store.clear();
  }

  @Test
  @DisplayName("4.0: konsument jest idempotentny po eventId (duplikat nie zwiększa liczby zapisów)")
  void shouldBeIdempotent() throws Exception {
    mockMvc.perform(post("/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{ \"productId\": 2, \"quantity\": 2 }"))
        .andExpect(status().isCreated());

    assertTrue(waitUntil(() -> store.size() == 1, 1000), "Expected 1 event after order create");

    OrderCreatedEvent e = store.getEvents().get(0);

    // publikujemy duplikat dokładnie tego samego eventu
    broker.publish("orders.created", e);

    // czekamy chwilę i upewniamy się, że nadal jest 1
    assertTrue(waitUntil(() -> store.size() == 1, 500), "Expected still 1 event after duplicate publish");
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
