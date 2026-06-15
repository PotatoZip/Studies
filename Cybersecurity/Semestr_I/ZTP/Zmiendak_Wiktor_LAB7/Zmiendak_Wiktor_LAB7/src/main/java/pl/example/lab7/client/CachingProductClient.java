package pl.example.lab7.client;

import pl.example.lab7.domain.ProductView;

import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;

public class CachingProductClient implements ProductClient {

    private final ProductClient delegate;
    private final Map<Long, ProductView> cache = new ConcurrentHashMap<>();

    public CachingProductClient(ProductClient delegate) {
        this.delegate = Objects.requireNonNull(delegate);
    }

    public ProductClient delegate() {
        return delegate;
    }

    @Override
    public ProductView getProduct(long productId) {
        return cache.computeIfAbsent(productId, delegate::getProduct);
    }

    @Override
    public void reserve(long productId, int quantity) {
        delegate.reserve(productId, quantity);
        cache.remove(productId);
    }
}
