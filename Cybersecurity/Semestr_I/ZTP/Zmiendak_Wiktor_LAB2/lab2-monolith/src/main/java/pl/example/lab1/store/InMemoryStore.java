package pl.example.lab1.store;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import pl.example.lab1.model.Product;
import pl.example.lab1.model.ShopOrder;

import java.util.LinkedHashMap;
import java.util.Map;

@Component
public class InMemoryStore {

    private final Map<Long, Product> products = new LinkedHashMap<>();
    private final Map<Long, ShopOrder> orders = new LinkedHashMap<>();

    private long nextProductId = 1L;
    private long nextOrderId = 1L;

    @PostConstruct
    public void init() {
        resetToDefaults();
    }

    public synchronized void resetToDefaults() {
        products.clear();
        orders.clear();

        products.put(1L, new Product(1L, "Klawiatura", 120.0, 10));
        products.put(2L, new Product(2L, "Mysz", 80.0, 15));
        nextProductId = 3L;

        orders.put(1L, new ShopOrder(1L, 1L, 2, 240.0, "2025-01-01T10:00:00Z"));
        nextOrderId = 2L;
    }

    public synchronized long generateNextProductId() { return nextProductId++; }
    public synchronized long generateNextOrderId() { return nextOrderId++; }

    public Map<Long, Product> getProducts() { return products; }
    public Map<Long, ShopOrder> getOrders() { return orders; }
}
