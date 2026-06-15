package pl.example.lab5.service;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import pl.example.lab5.dto.CreateOrderRequest;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.model.Order;
import pl.example.lab5.model.Product;
import pl.example.lab5.store.OrderStore;
import pl.example.lab5.store.ProductCatalog;

import java.util.UUID;

@Service
public class OrderService {

  private final ProductCatalog catalog;
  private final OrderStore orderStore;
  private final OrderEventPublisher publisher;

  public OrderService(ProductCatalog catalog, OrderStore orderStore, OrderEventPublisher publisher) {
    this.catalog = catalog;
    this.orderStore = orderStore;
    this.publisher = publisher;
  }

  public Order create(CreateOrderRequest req) {
    Product p = catalog.getProducts().get(req.getProductId());
    if (p == null) throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found");

    double total = p.getPrice() * req.getQuantity();
    long id = orderStore.nextId();
    Order order = new Order(id, req.getProductId(), req.getQuantity(), total);
    orderStore.getOrders().put(id, order);

    OrderCreatedEvent event = new OrderCreatedEvent(UUID.randomUUID().toString(), id, req.getProductId(), req.getQuantity(), total);

    publisher.publishOrderCreated(event);

    return order;
  }
}
