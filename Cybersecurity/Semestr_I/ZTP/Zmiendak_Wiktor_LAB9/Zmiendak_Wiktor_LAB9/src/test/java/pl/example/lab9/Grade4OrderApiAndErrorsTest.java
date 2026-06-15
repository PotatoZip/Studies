package pl.example.lab9;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import pl.example.lab9.contracts.ProductClient;
import pl.example.lab9.contracts.ProductDetails;
import pl.example.lab9.productservice.InsufficientStockException;
import pl.example.lab9.productservice.ProductNotFoundException;

import java.math.BigDecimal;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Grade4OrderApiAndErrorsTest {

  @Autowired
  MockMvc mvc;

  @MockBean
  ProductClient productClient;

  @Test
  @DisplayName("4.0 Order API creates order through ProductClient")
  void createOrderViaApi() throws Exception {
    when(productClient.getProduct(5L)).thenReturn(new ProductDetails(5L, "Keyboard", BigDecimal.valueOf(120), 8));

    mvc.perform(post("/order-service/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":5,\"quantity\":3}"))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.productId").value(5))
        .andExpect(jsonPath("$.productName").value("Keyboard"))
        .andExpect(jsonPath("$.quantity").value(3))
        .andExpect(jsonPath("$.total").value(360))
        .andExpect(jsonPath("$.createdAt").exists());

    verify(productClient).getProduct(5L);
    verify(productClient).reserveProduct(5L, 3);
  }

  @Test
  @DisplayName("4.0 Order API validates request body")
  void orderValidation() throws Exception {
    mvc.perform(post("/order-service/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":5,\"quantity\":0}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").exists());

    verifyNoInteractions(productClient);
  }

  @Test
  @DisplayName("4.0 Product not found from ProductClient maps to 404")
  void productMissingMapsTo404() throws Exception {
    when(productClient.getProduct(999L)).thenThrow(new ProductNotFoundException("Product not found"));

    mvc.perform(post("/order-service/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":999,\"quantity\":1}"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Product not found"));
  }

  @Test
  @DisplayName("4.0 Insufficient stock from ProductClient maps to 409 and does not save order")
  void insufficientStockMapsTo409AndNoOrderSaved() throws Exception {
    when(productClient.getProduct(5L)).thenReturn(new ProductDetails(5L, "Keyboard", BigDecimal.valueOf(120), 1));
    doThrow(new InsufficientStockException("Insufficient stock")).when(productClient).reserveProduct(5L, 2);

    mvc.perform(post("/order-service/orders")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"productId\":5,\"quantity\":2}"))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.error").value("Insufficient stock"));

    mvc.perform(get("/order-service/orders"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.length()").value(0));
  }
}
