package pl.example.lab5.store;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import pl.example.lab5.model.Product;

import java.util.LinkedHashMap;
import java.util.Map;

@Component
public class ProductCatalog {

  private final Map<Long, Product> products = new LinkedHashMap<>();

  @PostConstruct
  public void init() {
    products.put(1L, new Product(1L, "Klawiatura", 120.0, 10));
    products.put(2L, new Product(2L, "Mysz", 80.0, 15));
  }

  public Map<Long, Product> getProducts() {
    return products;
  }
}
