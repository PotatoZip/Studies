package pl.example.lab1.controller;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import pl.example.lab1.dto.OrderCreateRequest;
import pl.example.lab1.dto.ProductCreateRequest;
import pl.example.lab1.model.Product;
import pl.example.lab1.model.ShopOrder;
import pl.example.lab1.service.ShopService;

import java.util.List;
import java.util.Map;

@RestController
public class ShopController {

    private final ShopService shopService;

    public ShopController(ShopService shopService) {
        this.shopService = shopService;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "ok");
    }

    @GetMapping("/products")
    public List<Product> getProducts() {
        return shopService.getProducts();
    }

    @GetMapping("/products/{id}")
    public Product getProductById(@PathVariable long id) {
        return shopService.getProductById(id);
    }

    @PostMapping("/products")
    @ResponseStatus(HttpStatus.CREATED)
    public Product createProduct(@Valid @RequestBody ProductCreateRequest request) {
        return shopService.createProduct(request);
    }

    @GetMapping("/orders")
    public List<ShopOrder> getOrders() {
        return shopService.getOrders();
    }

    @GetMapping("/orders/{id}")
    public ShopOrder getOrderById(@PathVariable long id) {
        return shopService.getOrderById(id);
    }

    @PostMapping("/orders")
    @ResponseStatus(HttpStatus.CREATED)
    public ShopOrder createOrder(@Valid @RequestBody OrderCreateRequest request) {
        return shopService.createOrder(request);
    }

    // ====== helpery ======
    private String asString(Object value) {
        return value == null ? null : String.valueOf(value).trim();
    }

    private double asDouble(Object value, double defaultValue) {
        if (value instanceof Number n)
            return n.doubleValue();
        try {
            return value == null ? defaultValue : Double.parseDouble(String.valueOf(value));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    private int asInt(Object value, int defaultValue) {
        if (value instanceof Number n)
            return n.intValue();
        try {
            return value == null ? defaultValue : Integer.parseInt(String.valueOf(value));
        } catch (Exception e) {
            return defaultValue;
        }
    }

    private Long asLongObject(Object value) {
        if (value instanceof Number n)
            return n.longValue();
        try {
            return value == null ? null : Long.parseLong(String.valueOf(value));
        } catch (Exception e) {
            return null;
        }
    }
}
