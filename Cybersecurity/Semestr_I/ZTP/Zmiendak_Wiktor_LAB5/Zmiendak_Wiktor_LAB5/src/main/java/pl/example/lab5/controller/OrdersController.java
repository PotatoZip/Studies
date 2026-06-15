package pl.example.lab5.controller;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import pl.example.lab5.dto.CreateOrderRequest;
import pl.example.lab5.model.Order;
import pl.example.lab5.service.OrderService;

@RestController
public class OrdersController {

  private final OrderService orderService;

  public OrdersController(OrderService orderService) {
    this.orderService = orderService;
  }

  @PostMapping("/orders")
  @ResponseStatus(HttpStatus.CREATED)
  public Order create(@Valid @RequestBody CreateOrderRequest req) {
    return orderService.create(req);
  }
}
