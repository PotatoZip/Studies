package pl.example.lab7.service;

import pl.example.lab7.client.ProductClient;
import pl.example.lab7.domain.Order;
import pl.example.lab7.domain.ProductView;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicLong;

public class OrderService {
    private final ProductClient productClient;
    private final Clock clock;
    private final AtomicLong idSeq = new AtomicLong(100);

    public OrderService(ProductClient productClient, Clock clock) {
        this.productClient = Objects.requireNonNull(productClient);
        this.clock = Objects.requireNonNull(clock);
    }

    public Order placeOrder(long productId, int quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be > 0");
        }
        ProductView product = productClient.getProduct(productId);
        productClient.reserve(productId, quantity);
        return new Order(idSeq.incrementAndGet(), productId, quantity, total(product, quantity), now());
    }

    private static BigDecimal total(ProductView p, int quantity) {
        return p.price().multiply(BigDecimal.valueOf(quantity));
    }

    private Instant now() {
        return clock.instant();
    }
}
