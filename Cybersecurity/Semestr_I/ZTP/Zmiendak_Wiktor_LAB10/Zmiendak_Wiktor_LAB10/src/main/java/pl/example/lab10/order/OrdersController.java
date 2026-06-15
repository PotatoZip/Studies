package pl.example.lab10.order;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import pl.example.lab10.order.dto.CreateOrderRequest;

import java.util.List;

@RestController
public class OrdersController {

  private final OrderService orderService;

  public OrdersController(OrderService orderService) {
    this.orderService = orderService;
  }

  @PostMapping("/orders")
  public ResponseEntity<Order> createOrder(@Valid @RequestBody CreateOrderRequest request) {
    Order order = orderService.createOrder(request.getProductId(), request.getQuantity());
    return ResponseEntity.status(HttpStatus.CREATED).body(order);
  }

  @GetMapping("/orders/{id}")
  public Order getOrder(@PathVariable long id) {
    return orderService.getOrder(id);
  }

  @GetMapping("/orders")
  public List<Order> getOrders() {
    return orderService.getOrders();
  }
}
