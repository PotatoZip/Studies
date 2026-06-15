package pl.example.lab9.orderservice;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pl.example.lab9.orderservice.dto.CreateOrderRequest;

import java.util.List;

@RestController
@RequestMapping("/order-service/orders")
public class OrdersController {

  private final OrderService orderService;

  public OrdersController(OrderService orderService) {
    this.orderService = orderService;
  }

  @PostMapping
  public ResponseEntity<Order> createOrder(@Valid @RequestBody CreateOrderRequest request) {
    Order created = orderService.createOrder(request.getProductId(), request.getQuantity());
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
  }

  @GetMapping("/{id}")
  public Order getOrder(@PathVariable long id) {
    return orderService.getOrder(id);
  }

  @GetMapping
  public List<Order> getOrders() {
    return orderService.getOrders();
  }
}
