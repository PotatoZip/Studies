package pl.example.lab10.order;

import org.springframework.stereotype.Service;
import pl.example.lab10.events.OrderCreatedEvent;
import pl.example.lab10.outbox.OutboxStore;

import java.time.Clock;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Service
public class OrderServiceImpl implements OrderService {

  private final OrderStore orderStore;
  private final OutboxStore outboxStore;
  private final Clock clock;

  public OrderServiceImpl(OrderStore orderStore, OutboxStore outboxStore, Clock clock) {
    this.orderStore = orderStore;
    this.outboxStore = outboxStore;
    this.clock = clock;
  }

  @Override
  public Order createOrder(long productId, int quantity) {
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be > 0");
    }

    Instant now = Instant.now(clock);
    Order order = orderStore.create(productId, quantity, now);

    OrderCreatedEvent event = new OrderCreatedEvent(
        UUID.randomUUID().toString(),
        now,
        order.getId(),
        productId,
        quantity);

    outboxStore.save("orders.created", event, now);
    return order;
  }

  @Override
  public Order getOrder(long id) {
    return orderStore.findById(id)
        .orElseThrow(() -> new OrderNotFoundException("Order not found"));
  }

  @Override
  public List<Order> getOrders() {
    return orderStore.findAll();
  }
}
