package pl.example.lab10.product;

import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class ProductCatalog {

  private final AtomicLong sequence = new AtomicLong(1);
  private final ConcurrentMap<Long, Product> products = new ConcurrentHashMap<>();

  public Product create(String name, int stock) {
    if (name == null || name.isBlank()) {
      throw new IllegalArgumentException("Product name must not be blank");
    }
    if (stock < 0) {
      throw new IllegalArgumentException("Stock must be >= 0");
    }

    long id = sequence.getAndIncrement();
    Product product = new Product(id, name, stock);
    products.put(id, product);
    return product;
  }

  public Optional<Product> findById(long id) {
    return Optional.ofNullable(products.get(id));
  }

  public List<Product> findAll() {
    return new ArrayList<>(products.values()).stream()
        .sorted(Comparator.comparingLong(Product::getId))
        .toList();
  }

  public synchronized Product reserve(long productId, int quantity) {
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be > 0");
    }

    Product product = findById(productId)
        .orElseThrow(() -> new ProductNotFoundException("Product not found"));

    if (product.getStock() < quantity) {
      throw new InsufficientStockException("Insufficient stock");
    }

    product.decreaseStock(quantity);
    return product;
  }
}
