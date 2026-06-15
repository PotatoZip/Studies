package pl.example.lab7.domain;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Objects;

public record Order(long id, long productId, int quantity, BigDecimal total, Instant createdAt) {
    public Order {
        Objects.requireNonNull(total, "total");
        Objects.requireNonNull(createdAt, "createdAt");
    }
}
