package pl.example.lab9;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab9.contracts.ProductClient;
import pl.example.lab9.orderservice.OrderServiceImpl;
import pl.example.lab9.productservice.ProductService;
import pl.example.lab9.productservice.ProductServiceImpl;
import pl.example.lab9.productservice.ProductStore;

import java.lang.reflect.Field;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class Grade3ArchitectureTest {

  @Test
  @DisplayName("3.0 Contract classes exist")
  void contractClassesExist() throws Exception {
    Class.forName("pl.example.lab9.contracts.ProductClient");
    Class.forName("pl.example.lab9.contracts.ProductDetails");
    Class.forName("pl.example.lab9.contracts.ReserveProductCommand");
  }

  @Test
  @DisplayName("3.0 OrderService depends on ProductClient contract")
  void orderServiceUsesProductClient() {
    Field[] fields = OrderServiceImpl.class.getDeclaredFields();

    assertTrue(Arrays.stream(fields).anyMatch(field -> field.getType().equals(ProductClient.class)),
        "OrderServiceImpl should depend on ProductClient contract");
  }

  @Test
  @DisplayName("3.0 OrderService does not depend on product internals")
  void orderServiceDoesNotUseProductInternals() {
    Field[] fields = OrderServiceImpl.class.getDeclaredFields();

    for (Field field : fields) {
      assertNotEquals(ProductStore.class, field.getType(),
          "OrderServiceImpl must not depend directly on ProductStore");
      assertNotEquals(ProductService.class, field.getType(),
          "OrderServiceImpl must not depend directly on ProductService");
      assertNotEquals(ProductServiceImpl.class, field.getType(),
          "OrderServiceImpl must not depend directly on ProductServiceImpl");
    }
  }
}
