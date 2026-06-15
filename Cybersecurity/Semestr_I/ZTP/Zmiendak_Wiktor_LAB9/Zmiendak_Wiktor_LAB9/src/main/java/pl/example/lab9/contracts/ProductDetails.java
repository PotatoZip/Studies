package pl.example.lab9.contracts;

import java.math.BigDecimal;

public record ProductDetails(Long id, String name, BigDecimal price, int stock) {
}
