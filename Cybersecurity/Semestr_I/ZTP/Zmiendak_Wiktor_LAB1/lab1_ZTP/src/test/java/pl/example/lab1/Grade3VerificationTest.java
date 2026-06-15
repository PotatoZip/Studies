package pl.example.lab1;

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
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Grade3VerificationTest {

    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("3.0 /health -> 200 i {status: ok}")
    void healthEndpointShouldReturnOk() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.status").value("ok"));
    }

    @Test
    @DisplayName("3.0 GET /products/{id} -> istniejący produkt")
    void getProductByIdShouldReturnProduct() throws Exception {
        mockMvc.perform(get("/products/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Klawiatura"))
                .andExpect(jsonPath("$.price").value(120.0))
                .andExpect(jsonPath("$.stock").value(10));
    }

    @Test
    @DisplayName("3.0 GET /products/{id} -> 404 dla braku produktu")
    void getProductByIdShouldReturn404WhenMissing() throws Exception {
        mockMvc.perform(get("/products/999"))
                .andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.error").value("Product not found"));
    }

    @Test
    @DisplayName("3.0 POST /products -> walidacja (brak name)")
    void createProductShouldValidateName() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"price\": 100,
                                  \"stock\": 5
                                }
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").exists());
    }

    @Test
    @DisplayName("3.0 POST /products -> walidacja (price > 0, stock >= 0)")
    void createProductShouldValidatePriceAndStock() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"name\": \"Monitor\",
                                  \"price\": -1,
                                  \"stock\": -2
                                }
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").exists());
    }

    @Test
    @DisplayName("3.0 POST /products -> tworzy poprawny produkt")
    void createProductShouldCreateWhenValid() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"name\": \"Monitor\",
                                  \"price\": 999,
                                  \"stock\": 5
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(3))
                .andExpect(jsonPath("$.name").value("Monitor"))
                .andExpect(jsonPath("$.price").value(999.0))
                .andExpect(jsonPath("$.stock").value(5));
    }

    @Test
    @DisplayName("3.0 POST /orders -> 404 gdy produkt nie istnieje")
    void createOrderShouldReturn404WhenProductDoesNotExist() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"productId\": 999,
                                  \"quantity\": 1
                                }
                                """))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error").value("Product not found"));
    }

    @Test
    @DisplayName("3.0 POST /orders -> walidacja quantity > 0")
    void createOrderShouldValidateQuantity() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"productId\": 1,
                                  \"quantity\": 0
                                }
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").exists());
    }

    @Test
    @DisplayName("3.0 POST /orders -> poprawne total = price * quantity")
    void createOrderShouldCalculateTotal() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"productId\": 1,
                                  \"quantity\": 2
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.productId").value(1))
                .andExpect(jsonPath("$.quantity").value(2))
                .andExpect(jsonPath("$.total").value(240.0));
    }
}
