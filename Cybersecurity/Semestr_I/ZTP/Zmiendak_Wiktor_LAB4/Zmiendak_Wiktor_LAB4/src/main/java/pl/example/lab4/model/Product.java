package pl.example.lab4.model;

import java.math.BigDecimal;
import java.util.Objects;

public class Product {

    private final Long id;
    private final String name;
    private final BigDecimal price;
    private int stock;

    public Product(Long id, String name, BigDecimal price, int stock) {
        this.id = id;
        this.name = Objects.requireNonNull(name, "name must not be null");
        this.price = Objects.requireNonNull(price, "price must not be null");
        this.stock = stock;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public int getStock() {
        return stock;
    }

    public void decreaseStock(int quantity) {
        this.stock -= quantity;
    }
}
