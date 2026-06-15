package pl.example.lab9;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab9.contracts.ProductClient;
import pl.example.lab9.contracts.ProductDetails;
import pl.example.lab9.orderservice.Order;
import pl.example.lab9.orderservice.OrderNotFoundException;
import pl.example.lab9.orderservice.OrderServiceImpl;
import pl.example.lab9.orderservice.OrderStore;
import pl.example.lab9.productservice.InsufficientStockException;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade4OrderConsistencyTest {

  @Test
  @DisplayName("4.0 Failed reservation does not create order")
  void failedReservationHasNoSideEffects() {
    ProductClient client = mock(ProductClient.class);
    when(client.getProduct(3L)).thenReturn(new ProductDetails(3L, "SSD", BigDecimal.valueOf(250), 1));
    doThrow(new InsufficientStockException("Insufficient stock")).when(client).reserveProduct(3L, 2);

    OrderStore store = new OrderStore();
    Clock fixed = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    OrderServiceImpl service = new OrderServiceImpl(client, store, fixed);

    InsufficientStockException ex = assertThrows(InsufficientStockException.class, () -> service.createOrder(3L, 2));

    assertEquals("Insufficient stock", ex.getMessage());
    assertTrue(store.findAll().isEmpty(), "Order must not be saved when product reservation fails");
  }

  @Test
  @DisplayName("4.0 OrderService returns orders and missing order gives domain exception")
  void readsOrders() {
    ProductClient client = mock(ProductClient.class);
    when(client.getProduct(2L)).thenReturn(new ProductDetails(2L, "RAM", BigDecimal.valueOf(100), 10));

    Clock fixed = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
    OrderServiceImpl service = new OrderServiceImpl(client, new OrderStore(), fixed);

    Order first = service.createOrder(2L, 1);
    Order second = service.createOrder(2L, 2);

    assertEquals(first, service.getOrder(1L));
    assertEquals(second, service.getOrder(2L));

    List<Order> orders = service.getOrders();
    assertEquals(2, orders.size());
    assertEquals(1L, orders.get(0).id());
    assertEquals(2L, orders.get(1).id());

    OrderNotFoundException ex = assertThrows(OrderNotFoundException.class, () -> service.getOrder(999L));
    assertEquals("Order not found", ex.getMessage());
  }
}
