package pl.example.lab10;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class Grade4ApiWorkflowTest {

  @Autowired
  private MockMvc mockMvc;

  @Autowired
  private ObjectMapper objectMapper;

  @Test
  @DisplayName("E2E: produkt + zamówienie + outbox kończy się CONFIRMED i zmniejszonym stockiem")
  void apiWorkflowConfirmsOrderWhenStockIsAvailable() throws Exception {
    long productId = createProduct("Keyboard", 4);
    long orderId = createOrder(productId, 3);

    mockMvc.perform(post("/outbox/process"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.processed").value(1));

    mockMvc.perform(get("/orders/{id}", orderId))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("CONFIRMED"));

    mockMvc.perform(get("/products/{id}", productId))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.stock").value(1));
  }

  @Test
  @DisplayName("E2E: zbyt duża ilość kończy się REJECTED i nie zmniejsza stocku")
  void apiWorkflowRejectsOrderWhenStockIsInsufficient() throws Exception {
    long productId = createProduct("Mouse", 1);
    long orderId = createOrder(productId, 5);

    mockMvc.perform(post("/outbox/process"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.processed").value(1));

    mockMvc.perform(get("/orders/{id}", orderId))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("REJECTED"))
        .andExpect(jsonPath("$.rejectionReason").value("Insufficient stock"));

    mockMvc.perform(get("/products/{id}", productId))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.stock").value(1));
  }

  private long createProduct(String name, int stock) throws Exception {
    String json = """
        {
          "name": "%s",
          "stock": %d
        }
        """.formatted(name, stock);

    String response = mockMvc.perform(post("/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content(json))
        .andExpect(status().isCreated())
        .andReturn()
        .getResponse()
        .getContentAsString();

    JsonNode node = objectMapper.readTree(response);
    return node.get("id").asLong();
  }

  private long createOrder(long productId, int quantity) throws Exception {
    String json = """
        {
          "productId": %d,
          "quantity": %d
        }
        """.formatted(productId, quantity);

    String response = mockMvc.perform(post("/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content(json))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.status").value("PENDING"))
        .andReturn()
        .getResponse()
        .getContentAsString();

    JsonNode node = objectMapper.readTree(response);
    return node.get("id").asLong();
  }
}
