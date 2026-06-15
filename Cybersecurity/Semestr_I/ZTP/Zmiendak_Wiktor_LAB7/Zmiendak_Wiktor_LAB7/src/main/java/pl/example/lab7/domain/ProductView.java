package pl.example.lab7.domain;

import java.math.BigDecimal;
import java.util.Objects;

public record ProductView(long id, String name, BigDecimal price, int stock) {
    public ProductView {
        Objects.requireNonNull(name, "name");
        Objects.requireNonNull(price, "price");
    }
}
