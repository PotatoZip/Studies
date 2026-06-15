package pl.example.lab7;

import pl.example.lab7.client.CachingProductClient;
import pl.example.lab7.client.ProductClient;
import pl.example.lab7.domain.ProductView;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;

import static org.mockito.Mockito.*;

class Grade4CachingProductClientTest {

    @Test
    void caches_getProduct_calls() {
        ProductClient delegate = mock(ProductClient.class);
        when(delegate.getProduct(5L)).thenReturn(new ProductView(5L, "M", BigDecimal.ONE, 10));

        CachingProductClient client = new CachingProductClient(delegate);

        client.getProduct(5L);
        client.getProduct(5L);

        verify(delegate, times(1)).getProduct(5L);
    }

    @Test
    void reserve_invalidates_cache() {
        ProductClient delegate = mock(ProductClient.class);
        when(delegate.getProduct(5L)).thenReturn(new ProductView(5L, "M", BigDecimal.ONE, 10));

        CachingProductClient client = new CachingProductClient(delegate);

        client.getProduct(5L);
        client.reserve(5L, 1);
        client.getProduct(5L);

        verify(delegate, times(2)).getProduct(5L);
        verify(delegate, times(1)).reserve(5L, 1);
    }
}
