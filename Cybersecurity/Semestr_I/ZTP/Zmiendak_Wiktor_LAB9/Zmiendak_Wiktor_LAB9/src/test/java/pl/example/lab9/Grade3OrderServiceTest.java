package pl.example.lab9;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab9.contracts.ProductClient;
import pl.example.lab9.contracts.ProductDetails;
import pl.example.lab9.orderservice.Order;
import pl.example.lab9.orderservice.OrderServiceImpl;
import pl.example.lab9.orderservice.OrderStore;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade3OrderServiceTest {

  @Test
  @DisplayName("3.0 OrderService uses ProductClient, reserves stock and computes total")
  void createOrderUsesProductClient() {
    ProductClient client = mock(ProductClient.class);
    when(client.getProduct(7L)).thenReturn(new ProductDetails(7L, "Mouse", BigDecimal.valueOf(80), 10));

    Clock fixed = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    OrderServiceImpl service = new OrderServiceImpl(client, new OrderStore(), fixed);

    Order order = service.createOrder(7L, 2);

    assertEquals(1L, order.id());
    assertEquals(7L, order.productId());
    assertEquals("Mouse", order.productName());
    assertEquals(2, order.quantity());
    assertEquals(BigDecimal.valueOf(160), order.total());
    assertEquals(Instant.parse("2026-01-01T00:00:00Z"), order.createdAt());

    verify(client).getProduct(7L);
    verify(client).reserveProduct(7L, 2);
  }

  @Test
  @DisplayName("3.0 OrderService rejects non-positive quantity without calling ProductClient")
  void rejectsNonPositiveQuantity() {
    ProductClient client = mock(ProductClient.class);
    Clock fixed = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    OrderServiceImpl service = new OrderServiceImpl(client, new OrderStore(), fixed);

    IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> service.createOrder(1L, 0));

    assertEquals("Quantity must be > 0", ex.getMessage());
    verifyNoInteractions(client);
  }
}
