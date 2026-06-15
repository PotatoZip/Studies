package pl.example.lab9;

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
class Grade3ProductServiceContractTest {

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
  @DisplayName("3.0 Product service creates and reads product")
  void createAndReadProduct() throws Exception {
    mvc.perform(post("/product-service/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"name\":\"Monitor\",\"price\":999.00,\"stock\":5}"))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.name").value("Monitor"))
        .andExpect(jsonPath("$.price").value(999.00))
        .andExpect(jsonPath("$.stock").value(5));

    mvc.perform(get("/product-service/products/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.name").value("Monitor"));
  }

  @Test
  @DisplayName("3.0 Product service lists products sorted by id")
  void listProducts() throws Exception {
    mvc.perform(post("/product-service/products").contentType(MediaType.APPLICATION_JSON)
        .content("{\"name\":\"Mouse\",\"price\":80.00,\"stock\":10}"));
    mvc.perform(post("/product-service/products").contentType(MediaType.APPLICATION_JSON)
        .content("{\"name\":\"Keyboard\",\"price\":120.00,\"stock\":4}"));

    mvc.perform(get("/product-service/products"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.length()").value(2))
        .andExpect(jsonPath("$[0].name").value("Mouse"))
        .andExpect(jsonPath("$[1].name").value("Keyboard"));
  }

  @Test
  @DisplayName("3.0 Product service reserves product and decreases stock")
  void reserveProduct() throws Exception {
    mvc.perform(post("/product-service/products")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"name\":\"SSD\",\"price\":250.00,\"stock\":5}"))
        .andExpect(status().isCreated());

    mvc.perform(post("/product-service/products/1/reservations")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"quantity\":2}"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.stock").value(3));

    mvc.perform(get("/product-service/products/1"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.stock").value(3));
  }

  @Test
  @DisplayName("3.0 Product service returns 404 for missing product")
  void missingProduct() throws Exception {
    mvc.perform(get("/product-service/products/999"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Product not found"));
  }
}
