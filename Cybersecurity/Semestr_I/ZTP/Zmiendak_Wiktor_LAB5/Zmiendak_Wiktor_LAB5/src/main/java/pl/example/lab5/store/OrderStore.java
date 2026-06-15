package pl.example.lab5.store;

import org.springframework.stereotype.Component;
import pl.example.lab5.model.Order;

import java.util.LinkedHashMap;
import java.util.Map;

@Component
public class OrderStore {
  private final Map<Long, Order> orders = new LinkedHashMap<>();
  private long nextId = 1L;

  public synchronized long nextId() {
    return nextId++;
  }

  public Map<Long, Order> getOrders() {
    return orders;
  }
}
