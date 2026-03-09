package pl.example.lab1;

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
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Grade4VerificationTest {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ObjectMapper objectMapper;

    @Test
    @DisplayName("4.0 GET /orders/{id} -> istniejące zamówienie")
    void getOrderByIdShouldReturnOrder() throws Exception {
        mockMvc.perform(get("/orders/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.productId").value(1))
                .andExpect(jsonPath("$.quantity").value(2))
                .andExpect(jsonPath("$.total").value(240.0));
    }

    @Test
    @DisplayName("4.0 GET /orders/{id} -> 404 dla braku zamówienia")
    void getOrderByIdShouldReturn404WhenMissing() throws Exception {
        mockMvc.perform(get("/orders/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error").value("Order not found"));
    }

    @Test
    @DisplayName("4.0 POST /orders -> kontrola stanów magazynowych")
    void createOrderShouldRejectWhenInsufficientStock() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"productId\": 1,
                                  \"quantity\": 999
                                }
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Insufficient stock"));
    }

    @Test
    @DisplayName("4.0 POST /orders -> zmniejsza stock po poprawnym zamówieniu")
    void createOrderShouldDecreaseStock() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"productId\": 1,
                                  \"quantity\": 3
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.total").value(360.0));

        mockMvc.perform(get("/products/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.stock").value(7));
    }

    @Test
    @DisplayName("4.0 Nowe zamówienie można pobrać przez GET /orders/{id}")
    void createdOrderShouldBeReadableById() throws Exception {
        MvcResult result = mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  \"productId\": 2,
                                  \"quantity\": 2
                                }
                                """))
                .andExpect(status().isCreated())
                .andReturn();

        JsonNode node = objectMapper.readTree(result.getResponse().getContentAsString());
        int createdId = node.get("id").asInt();

        mockMvc.perform(get("/orders/" + createdId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(createdId))
                .andExpect(jsonPath("$.productId").value(2))
                .andExpect(jsonPath("$.quantity").value(2))
                .andExpect(jsonPath("$.total").value(160.0));
    }
}
