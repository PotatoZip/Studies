package pl.example.lab5;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import pl.example.lab5.store.ReceivedEventsStore;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class Grade3PublishAndConsumeTest {

  @Autowired MockMvc mockMvc;
  @Autowired ObjectMapper objectMapper;
  @Autowired ReceivedEventsStore receivedEventsStore;

  @BeforeEach
  void setup() {
    receivedEventsStore.clear();
  }

  @Test
  @DisplayName("3.0: POST /orders publikuje event orders.created i konsument go odbiera")
  void shouldPublishAndConsumeEvent() throws Exception {
    var res = mockMvc.perform(post("/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{ \"productId\": 1, \"quantity\": 2 }"))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.productId").value(1))
        .andExpect(jsonPath("$.quantity").value(2))
        .andExpect(jsonPath("$.total").value(240.0))
        .andReturn();

    // czekamy max 1s na asynchroniczne dostarczenie
    assertTrue(waitUntil(() -> receivedEventsStore.size() == 1, 1000),
        "Expected exactly 1 received event");

    mockMvc.perform(get("/notifications/events"))
        .andExpect(status().isOk())
        .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$[0].productId").value(1))
        .andExpect(jsonPath("$[0].quantity").value(2))
        .andExpect(jsonPath("$[0].total").value(240.0));
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
