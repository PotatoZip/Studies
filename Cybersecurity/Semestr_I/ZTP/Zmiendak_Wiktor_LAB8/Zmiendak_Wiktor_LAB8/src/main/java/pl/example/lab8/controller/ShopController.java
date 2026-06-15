package pl.example.lab8.controller;

import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import pl.example.lab8.dto.OrderCreateRequest;
import pl.example.lab8.dto.ProductCreateRequest;
import pl.example.lab8.entity.OrderEntity;
import pl.example.lab8.entity.ProductEntity;
import pl.example.lab8.service.ShopService;

import java.math.BigDecimal;
import java.util.Map;

@RestController
public class ShopController {

  private final ShopService service;

  public ShopController(ShopService service) {
    this.service = service;
  }

  @GetMapping("/health")
  public Map<String, String> health() {
    return Map.of("status", "ok");
  }

  @PostMapping("/products")
  @ResponseStatus(HttpStatus.CREATED)
  public ProductEntity createProduct(@Valid @RequestBody ProductCreateRequest req) {
    return service.createProduct(req);
  }

  @GetMapping("/products/{id}")
  public ProductEntity getProduct(@PathVariable long id) {
    return service.getProduct(id);
  }

  @GetMapping("/products/search")
  public Page<ProductEntity> searchProducts(
      @RequestParam String q,
      @RequestParam BigDecimal minPrice,
      @RequestParam BigDecimal maxPrice,
      Pageable pageable
  ) {
    return service.searchProducts(q, minPrice, maxPrice, pageable);
  }

  @PostMapping("/orders")
  @ResponseStatus(HttpStatus.CREATED)
  public OrderEntity createOrder(@Valid @RequestBody OrderCreateRequest req) {
    return service.createOrder(req);
  }

  @GetMapping("/orders/{id}")
  public OrderEntity getOrder(@PathVariable long id) {
    return service.getOrder(id);
  }

  @GetMapping("/orders")
  public Page<OrderEntity> listOrders(Pageable pageable) {
    return service.listOrders(pageable);
  }
}
