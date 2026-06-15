package pl.example.lab7.client;

import pl.example.lab7.domain.ProductView;
import pl.example.lab7.errors.ServiceUnavailableException;

import java.util.Objects;
import java.util.NoSuchElementException;

public class RetryingProductClient implements ProductClient {

    private final ProductClient delegate;
    private final int maxAttempts;

    public RetryingProductClient(ProductClient delegate, int maxAttempts) {
        this.delegate = Objects.requireNonNull(delegate);
        this.maxAttempts = maxAttempts;
    }

    public ProductClient delegate() {
        return delegate;
    }

    @Override
    public ProductView getProduct(long productId) {
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return delegate.getProduct(productId);
            } catch (ServiceUnavailableException e) {
                if (attempt == maxAttempts) {
                    throw new IllegalStateException("Product service unavailable");
                }
            } catch (NoSuchElementException | IllegalStateException e) {
                throw e;
            }
        }
        throw new IllegalStateException("Product service unavailable");
    }

    @Override
    public void reserve(long productId, int quantity) {
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                delegate.reserve(productId, quantity);
                return;
            } catch (ServiceUnavailableException e) {
                if (attempt == maxAttempts) {
                    throw new IllegalStateException("Product service unavailable");
                }
            } catch (NoSuchElementException | IllegalStateException e) {
                throw e;
            }
        }
        throw new IllegalStateException("Product service unavailable");
    }
}
