package pl.example.lab8;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Grade3JpaBasicsTest {

  @Autowired
  MockMvc mvc;

  @Test
  @DisplayName("3.0 /health -> {status: ok}")
  void health() throws Exception {
    mvc.perform(get("/health"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("ok"));
  }

  @Test
  @DisplayName("3.0 POST /products validates body")
  void productValidation() throws Exception {
    mvc.perform(post("/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"price\":10,\"stock\":1}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").exists());
  }

  @Test
  @DisplayName("3.0 Create product and read it back")
  void createAndGetProduct() throws Exception {
    mvc.perform(post("/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"name\":\"Monitor\",\"price\":999.00,\"stock\":5}"))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.name").value("Monitor"))
        .andExpect(jsonPath("$.price").value(999.00))
        .andExpect(jsonPath("$.stock").value(5));

    mvc.perform(get("/products/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.name").value("Monitor"));
  }

  @Test
  @DisplayName("3.0 POST /orders -> 404 when product missing")
  void orderProductMissing() throws Exception {
    mvc.perform(post("/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":999,\"quantity\":1}"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Product not found"));
  }

  @Test
  @DisplayName("3.0 POST /orders -> 400 when insufficient stock, and no side effects")
  void insufficientStockNoSideEffects() throws Exception {
    mvc.perform(post("/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"name\":\"Klawiatura\",\"price\":120.00,\"stock\":2}"))
        .andExpect(status().isCreated());

    mvc.perform(post("/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":1,\"quantity\":3}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").value("Insufficient stock"));

    mvc.perform(get("/products/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.stock").value(2));
  }

  @Test
  @DisplayName("3.0 Create order calculates total and decreases stock")
  void createOrderUpdatesStockAndTotal() throws Exception {
    mvc.perform(post("/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"name\":\"Mysz\",\"price\":80.00,\"stock\":10}"))
        .andExpect(status().isCreated());

    mvc.perform(post("/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":1,\"quantity\":2}"))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.productId").value(1))
        .andExpect(jsonPath("$.quantity").value(2))
        .andExpect(jsonPath("$.total").value(160.00))
        .andExpect(jsonPath("$.createdAt").exists());

    mvc.perform(get("/products/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.stock").value(8));

    mvc.perform(get("/orders/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.total").value(160.00));
  }

  @Test
  @DisplayName("3.0 GET /orders/{id} -> 404 when missing")
  void orderNotFound() throws Exception {
    mvc.perform(get("/orders/999"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Order not found"));
  }
}
