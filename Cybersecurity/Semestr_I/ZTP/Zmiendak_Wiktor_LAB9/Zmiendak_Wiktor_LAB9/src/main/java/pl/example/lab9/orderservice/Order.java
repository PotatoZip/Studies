package pl.example.lab9.orderservice;

import java.math.BigDecimal;
import java.time.Instant;

public record Order(
    Long id,
    Long productId,
    String productName,
    int quantity,
    BigDecimal total,
    Instant createdAt
) {
}
