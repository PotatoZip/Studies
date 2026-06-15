package pl.example.lab3;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import pl.example.lab3.entity.ProductEntity;
import pl.example.lab3.entity.ShopOrderEntity;
import pl.example.lab3.repository.ProductRepository;
import pl.example.lab3.repository.ShopOrderRepository;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Lab3Grade3PersistenceTest {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ProductRepository productRepository;

    @Autowired
    ShopOrderRepository shopOrderRepository;

    @Test
    @DisplayName("3.0/1 POST /products zapisuje produkt w repozytorium i GET /products go zwraca")
    void createProductShouldPersistInRepositoryAndBeVisibleInApi() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "name": "Monitor",
                                  "price": 999.0,
                                  "stock": 5
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Monitor"))
                .andExpect(jsonPath("$.price").value(999.0))
                .andExpect(jsonPath("$.stock").value(5));

        assertEquals(1, productRepository.count(), "Product should be saved in ProductRepository");

        ProductEntity savedProduct = productRepository.findById(1L).orElseThrow();
        assertEquals("Monitor", savedProduct.getName());
        assertEquals(999.0, savedProduct.getPrice());
        assertEquals(5, savedProduct.getStock());

        mockMvc.perform(get("/products"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1))
                .andExpect(jsonPath("$[0].name").value("Monitor"))
                .andExpect(jsonPath("$[0].price").value(999.0))
                .andExpect(jsonPath("$[0].stock").value(5));
    }

    @Test
    @DisplayName("3.0/2 POST /orders zapisuje zamówienie w repozytorium i GET /orders je zwraca")
    void createOrderShouldPersistInRepositoryAndBeVisibleInApi() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "name": "Klawiatura",
                                  "price": 120.0,
                                  "stock": 10
                                }
                                """))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "productId": 1,
                                  "quantity": 2
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.productId").value(1))
                .andExpect(jsonPath("$.quantity").value(2))
                .andExpect(jsonPath("$.total").value(240.0));

        assertEquals(1, shopOrderRepository.count(), "Order should be saved in ShopOrderRepository");

        ShopOrderEntity savedOrder = shopOrderRepository.findById(1L).orElseThrow();
        assertNotNull(savedOrder.getProduct(), "Saved order should reference a product entity");
        assertEquals(1L, savedOrder.getProduct().getId());
        assertEquals(2, savedOrder.getQuantity());
        assertEquals(240.0, savedOrder.getTotal());

        mockMvc.perform(get("/orders"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1))
                .andExpect(jsonPath("$[0].productId").value(1))
                .andExpect(jsonPath("$[0].quantity").value(2))
                .andExpect(jsonPath("$[0].total").value(240.0));
    }
}
