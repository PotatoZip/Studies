package pl.example.lab10.order;

import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class OrderStore {

  private final AtomicLong sequence = new AtomicLong(1);
  private final ConcurrentMap<Long, Order> orders = new ConcurrentHashMap<>();

  public Order create(long productId, int quantity, Instant createdAt) {
    long id = sequence.getAndIncrement();
    Order order = new Order(id, productId, quantity, createdAt);
    orders.put(id, order);
    return order;
  }

  public Optional<Order> findById(long id) {
    return Optional.ofNullable(orders.get(id));
  }

  public List<Order> findAll() {
    return new ArrayList<>(orders.values()).stream()
        .sorted(Comparator.comparingLong(Order::getId))
        .toList();
  }

  public Order confirm(long orderId) {
    Order order = findById(orderId)
        .orElseThrow(() -> new OrderNotFoundException("Order not found"));
    order.confirm();
    return order;
  }

  public Order reject(long orderId, String reason) {
    Order order = findById(orderId)
        .orElseThrow(() -> new OrderNotFoundException("Order not found"));
    order.reject(reason);
    return order;
  }
}
