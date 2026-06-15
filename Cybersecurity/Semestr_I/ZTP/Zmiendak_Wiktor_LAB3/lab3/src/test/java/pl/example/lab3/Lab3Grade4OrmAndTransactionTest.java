package pl.example.lab3;

import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;
import pl.example.lab3.dto.OrderCreateRequest;
import pl.example.lab3.entity.ProductEntity;
import pl.example.lab3.entity.ShopOrderEntity;
import pl.example.lab3.repository.ProductRepository;
import pl.example.lab3.repository.ShopOrderRepository;
import pl.example.lab3.service.ShopServiceImpl;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class Lab3Grade4OrmAndTransactionTest {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ProductRepository productRepository;

    @Autowired
    ShopOrderRepository shopOrderRepository;

    @Test
    @DisplayName("4.0/1 ShopOrderEntity ma relację @ManyToOne do produktu z @JoinColumn(name = \"product_id\")")
    void orderEntityShouldContainManyToOneRelationToProduct() throws Exception {
        Field productField = ShopOrderEntity.class.getDeclaredField("product");
        assertTrue(productField.isAnnotationPresent(ManyToOne.class),
                "Field 'product' in ShopOrderEntity must be annotated with @ManyToOne");

        JoinColumn joinColumn = productField.getAnnotation(JoinColumn.class);
        assertNotNull(joinColumn, "Field 'product' in ShopOrderEntity must have @JoinColumn");
        assertEquals("product_id", joinColumn.name(),
                "Join column for product relation should be named 'product_id'");
    }

    @Test
    @DisplayName("4.0/2 createOrder jest transakcyjne")
    void createOrderShouldBeTransactional() throws Exception {
        Method method = ShopServiceImpl.class.getDeclaredMethod("createOrder", OrderCreateRequest.class);

        boolean methodTransactional = method.isAnnotationPresent(Transactional.class);
        boolean classTransactional = ShopServiceImpl.class.isAnnotationPresent(Transactional.class);

        assertTrue(methodTransactional || classTransactional,
                "ShopServiceImpl.createOrder(...) should be transactional");
    }

    @Test
    @DisplayName("4.0/3 GET /products/{id} zwraca 404 i JSON z błędem dla brakującego produktu")
    void getProductByIdShouldReturn404WhenMissing() throws Exception {
        mockMvc.perform(get("/products/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error").value("Product not found"));
    }

    @Test
    @DisplayName("4.0/4 POST /orders zwraca 404 dla brakującego produktu i nie zapisuje zamówienia")
    void createOrderShouldReturn404WhenProductMissingAndNotPersistAnything() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "productId": 999,
                                  "quantity": 1
                                }
                                """))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.error").value("Product not found"));

        assertEquals(0, shopOrderRepository.count(), "Order should not be saved when product does not exist");
    }

    @Test
    @DisplayName("4.0/5 POST /orders zwraca 400 przy zbyt małym stock i nie zmienia stanu bazy")
    void createOrderShouldRejectWhenInsufficientStockAndKeepStateUnchanged() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "name": "Mysz",
                                  "price": 80.0,
                                  "stock": 3
                                }
                                """))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "productId": 1,
                                  "quantity": 10
                                }
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Insufficient stock"));

        assertEquals(0, shopOrderRepository.count(), "Order should not be saved when stock is insufficient");

        ProductEntity product = productRepository.findById(1L).orElseThrow();
        assertEquals(3, product.getStock(), "Product stock should remain unchanged after rejected order");
    }

    @Test
    @DisplayName("4.0/6 Poprawne zamówienie zmniejsza stock, zapisuje createdAt i jest dostępne przez GET /orders/{id}")
    void successfulOrderShouldDecreaseStockPersistCreatedAtAndBeAccessibleById() throws Exception {
        mockMvc.perform(post("/products")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "name": "Laptop",
                                  "price": 3000.0,
                                  "stock": 5
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
                .andExpect(jsonPath("$.total").value(6000.0))
                .andExpect(jsonPath("$.createdAt").isNotEmpty());

        ProductEntity updatedProduct = productRepository.findById(1L).orElseThrow();
        assertEquals(3, updatedProduct.getStock(), "Product stock should be decreased after a successful order");

        ShopOrderEntity savedOrder = shopOrderRepository.findById(1L).orElseThrow();
        assertNotNull(savedOrder.getCreatedAt(), "createdAt should be persisted in ShopOrderEntity");

        mockMvc.perform(get("/orders/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.productId").value(1))
                .andExpect(jsonPath("$.quantity").value(2))
                .andExpect(jsonPath("$.total").value(6000.0))
                .andExpect(jsonPath("$.createdAt").isNotEmpty());
    }
}
