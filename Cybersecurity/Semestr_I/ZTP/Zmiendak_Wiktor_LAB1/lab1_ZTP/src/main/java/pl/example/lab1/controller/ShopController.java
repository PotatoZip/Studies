package pl.example.lab1.controller;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import pl.example.lab1.model.Product;
import pl.example.lab1.model.ShopOrder;
import pl.example.lab1.store.InMemoryStore;

import java.time.Instant;
import java.util.Collections;
import java.util.List;
import java.util.Map;

@RestController
public class ShopController {

    private final InMemoryStore store;

    public ShopController(InMemoryStore store) {
        this.store = store;
    }

    @GetMapping("/")
    public Map<String, Object> index() {
        return Map.of(
                "service", "Monolith Shop API",
                "version", "0.1",
                "endpoints", List.of(
                        "GET /products",
                        "POST /products",
                        "GET /orders",
                        "POST /orders",
                        "GET /health"));
    }

    // TODO (3.0): dodać GET /health

    @GetMapping("/health")
    public Map<String, Object> health() {
        return Map.of("status", "ok");
    }

    @GetMapping("/products")
    public List<Product> getProducts() {
        return store.getProducts().values().stream().toList();
    }

    // TODO (3.0): dodać GET /products/{id}

    @GetMapping("/products/{id}")
    public Product getProductById(@PathVariable long id) {
        Product product = store.getProducts().get(id);
        if (product == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found");
        }
        return product;
    }

    @PostMapping("/products")
    @ResponseStatus(HttpStatus.CREATED)
    public Product createProduct(@RequestBody(required = false) Map<String, Object> body) {
        Map<String, Object> data = body == null ? Collections.emptyMap() : body;

        String name = asString(data.get("name"));
        if (name == null || name.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "name is required");
        }

        double price = asDouble(data.get("price"), -1.0);
        if (price <= 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "price must be > 0");
        }

        int stock = asInt(data.get("stock"), -1);
        if (stock < 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "stock must be >= 0");
        }

        long id = store.generateNextProductId();
        Product product = new Product(id, name, price, stock);
        store.getProducts().put(id, product);
        return product;
    }

    @GetMapping("/orders")
    public List<ShopOrder> getOrders() {
        return store.getOrders().values().stream().toList();
    }

    // TODO (4.0): dodać GET /orders/{id}

    @GetMapping("/orders/{id}")
    public ShopOrder getOrderById(@PathVariable long id) {
        ShopOrder order = store.getOrders().get(id);
        if (order == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found");
        }
        return order;
    }

    @PostMapping("/orders")
    @ResponseStatus(HttpStatus.CREATED)
    public ShopOrder createOrder(@RequestBody(required = false) Map<String, Object> body) {
        Map<String, Object> data = body == null ? Collections.emptyMap() : body;

        Long productId = asLongObject(data.get("productId"));
        if (productId == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "productId is required");
        }

        int quantity = asInt(data.get("quantity"), -1);
        if (quantity <= 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "quantity must be > 0");
        }

        Product product = store.getProducts().get(productId);
        if (product == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found");
        }

        if (quantity > product.getStock()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Insufficient stock");
        }

        double price = product.getPrice();
        if (price <= 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Product has invalid price");
        }

        double total = price * quantity;

        long orderId = store.generateNextOrderId();
        ShopOrder order = new ShopOrder(
                orderId,
                productId,
                quantity,
                total,
                Instant.now().toString());

        product.setStock(product.getStock() - quantity);

        store.getOrders().put(orderId, order);
        return order;
    }

    // ====== Helpery (celowo proste) ======

    private String asString(Object value) {
        return value == null ? null : String.valueOf(value).trim();
    }

    private double asDouble(Object value, double defaultValue) {
        if (value instanceof Number n) {
            return n.doubleValue();
        }
        try {
            return value == null ? defaultValue : Double.parseDouble(String.valueOf(value));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    private int asInt(Object value, int defaultValue) {
        if (value instanceof Number n) {
            return n.intValue();
        }
        try {
            return value == null ? defaultValue : Integer.parseInt(String.valueOf(value));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    private Long asLongObject(Object value) {
        if (value instanceof Number n) {
            return n.longValue();
        }
        try {
            return value == null ? null : Long.parseLong(String.valueOf(value));
        } catch (Exception e) {
            return null;
        }
    }
}
