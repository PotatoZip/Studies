package pl.example.lab9.orderservice;

import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.Instant;
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

  public synchronized Order create(Long productId, String productName, int quantity, BigDecimal total, Instant createdAt) {
    Long id = sequence.getAndIncrement();
    Order order = new Order(id, productId, productName, quantity, total, createdAt);
    orders.put(id, order);
    return order;
  }

  public Optional<Order> findById(Long id) {
    return Optional.ofNullable(orders.get(id));
  }

  public List<Order> findAll() {
    return orders.values().stream()
        .sorted(Comparator.comparing(Order::id))
        .toList();
  }

  public synchronized void clear() {
    orders.clear();
    sequence.set(1);
  }
}
