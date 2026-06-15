package pl.example.lab7;

import pl.example.lab7.client.ProductClient;
import pl.example.lab7.domain.Order;
import pl.example.lab7.domain.ProductView;
import pl.example.lab7.service.OrderService;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade3OrderServiceTest {

    @Test
    void placeOrder_usesProductClient_andComputesTotal() {
        ProductClient client = mock(ProductClient.class);
        when(client.getProduct(7L)).thenReturn(new ProductView(7L, "Mouse", BigDecimal.valueOf(80), 10));

        Clock fixed = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
        OrderService service = new OrderService(client, fixed);

        Order order = service.placeOrder(7L, 2);

        assertEquals(7L, order.productId());
        assertEquals(2, order.quantity());
        assertEquals(BigDecimal.valueOf(160), order.total());
        assertEquals(Instant.parse("2026-01-01T00:00:00Z"), order.createdAt());

        verify(client).getProduct(7L);
        verify(client).reserve(7L, 2);
    }

    @Test
    void placeOrder_rejectsNonPositiveQuantity() {
        ProductClient client = mock(ProductClient.class);
        Clock fixed = Clock.fixed(Instant.parse("2026-01-01T00:00:00Z"), ZoneOffset.UTC);
        OrderService service = new OrderService(client, fixed);

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> service.placeOrder(1L, 0));
        assertEquals("Quantity must be > 0", ex.getMessage());
        verifyNoInteractions(client);
    }
}
