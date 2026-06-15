package pl.example.lab9.orderservice;

import org.springframework.stereotype.Service;
import pl.example.lab9.contracts.ProductClient;

import java.time.Clock;
import java.util.List;

@Service
public class OrderServiceImpl implements OrderService {

  private final ProductClient productClient;
  private final OrderStore orderStore;
  private final Clock clock;

  public OrderServiceImpl(ProductClient productClient, OrderStore orderStore, Clock clock) {
    this.productClient = productClient;
    this.orderStore = orderStore;
    this.clock = clock;
  }

  @Override
  public Order createOrder(long productId, int quantity) {
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be > 0");
    }

    var product = productClient.getProduct(productId);
    productClient.reserveProduct(productId, quantity);

    var total = product.price().multiply(java.math.BigDecimal.valueOf(quantity));
    return orderStore.create(product.id(), product.name(), quantity, total, java.time.Instant.now(clock));
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
