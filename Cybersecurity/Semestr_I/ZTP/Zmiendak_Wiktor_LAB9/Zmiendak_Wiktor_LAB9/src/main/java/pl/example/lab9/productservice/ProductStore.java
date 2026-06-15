package pl.example.lab9.productservice;

import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class ProductStore {

  private final AtomicLong sequence = new AtomicLong(1);
  private final ConcurrentMap<Long, Product> products = new ConcurrentHashMap<>();

  public synchronized Product create(String name, BigDecimal price, int stock) {
    Long id = sequence.getAndIncrement();
    Product product = new Product(id, name, price, stock);
    products.put(id, product);
    return product;
  }

  public Optional<Product> findById(Long id) {
    return Optional.ofNullable(products.get(id));
  }

  public List<Product> findAll() {
    return products.values().stream()
        .sorted(Comparator.comparing(Product::getId))
        .toList();
  }

  public synchronized void clear() {
    products.clear();
    sequence.set(1);
  }
}
