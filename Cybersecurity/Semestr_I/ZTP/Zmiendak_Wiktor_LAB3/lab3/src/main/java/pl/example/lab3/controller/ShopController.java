package pl.example.lab3.controller;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import pl.example.lab3.dto.OrderCreateRequest;
import pl.example.lab3.dto.ProductCreateRequest;
import pl.example.lab3.model.Product;
import pl.example.lab3.model.ShopOrder;
import pl.example.lab3.service.ShopService;

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
    public Product getProductById(@PathVariable Long id) {
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
    public ShopOrder getOrderById(@PathVariable Long id) {
        return shopService.getOrderById(id);
    }

    @PostMapping("/orders")
    @ResponseStatus(HttpStatus.CREATED)
    public ShopOrder createOrder(@Valid @RequestBody OrderCreateRequest request) {
        return shopService.createOrder(request);
    }
}
