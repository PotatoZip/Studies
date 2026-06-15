package pl.example.lab7;

import pl.example.lab7.client.ProductClient;
import pl.example.lab7.client.RetryingProductClient;
import pl.example.lab7.domain.ProductView;
import pl.example.lab7.errors.ServiceUnavailableException;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade4RetryingProductClientTest {

    @Test
    void retries_onServiceUnavailable_thenSucceeds() {
        ProductClient delegate = mock(ProductClient.class);
        when(delegate.getProduct(1L))
                .thenThrow(new ServiceUnavailableException("503"))
                .thenThrow(new ServiceUnavailableException("503"))
                .thenReturn(new ProductView(1L, "K", BigDecimal.TEN, 1));

        RetryingProductClient client = new RetryingProductClient(delegate, 3);
        ProductView pv = client.getProduct(1L);

        assertEquals(1L, pv.id());
        verify(delegate, times(3)).getProduct(1L);
    }

    @Test
    void doesNotRetry_onBusinessNotFound() {
        ProductClient delegate = mock(ProductClient.class);
        when(delegate.getProduct(1L)).thenThrow(new NoSuchElementException("Product not found"));

        RetryingProductClient client = new RetryingProductClient(delegate, 3);
        assertThrows(NoSuchElementException.class, () -> client.getProduct(1L));
        verify(delegate, times(1)).getProduct(1L);
    }

    @Test
    void whenAllAttemptsFail_throwServiceUnavailableMessage() {
        ProductClient delegate = mock(ProductClient.class);
        when(delegate.getProduct(1L)).thenThrow(new ServiceUnavailableException("503"));

        RetryingProductClient client = new RetryingProductClient(delegate, 2);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> client.getProduct(1L));
        assertEquals("Product service unavailable", ex.getMessage());
        verify(delegate, times(2)).getProduct(1L);
    }
}
