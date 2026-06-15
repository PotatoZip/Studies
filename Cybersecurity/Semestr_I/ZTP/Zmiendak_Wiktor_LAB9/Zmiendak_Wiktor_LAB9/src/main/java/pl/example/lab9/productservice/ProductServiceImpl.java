package pl.example.lab9.productservice;

import org.springframework.stereotype.Service;
import pl.example.lab9.contracts.ProductDetails;
import pl.example.lab9.productservice.dto.CreateProductRequest;

import java.util.List;

@Service
public class ProductServiceImpl implements ProductService {

  private final ProductStore store;

  public ProductServiceImpl(ProductStore store) {
    this.store = store;
  }

  @Override
  public ProductDetails createProduct(CreateProductRequest request) {
    Product product = store.create(request.getName(), request.getPrice(), request.getStock());
    return toDetails(product);
  }

  @Override
  public ProductDetails getProduct(long id) {
    return store.findById(id)
        .map(this::toDetails)
        .orElseThrow(() -> new ProductNotFoundException("Product not found"));
  }

  @Override
  public List<ProductDetails> getProducts() {
    return store.findAll().stream()
        .map(this::toDetails)
        .toList();
  }

  @Override
  public ProductDetails reserveProduct(long id, int quantity) {
    if (quantity <= 0) {
      throw new IllegalArgumentException("Quantity must be > 0");
    }

    Product product = store.findById(id)
        .orElseThrow(() -> new ProductNotFoundException("Product not found"));

    if (product.getStock() < quantity) {
      throw new InsufficientStockException("Insufficient stock");
    }

    product.decreaseStock(quantity);
    return toDetails(product);
  }

  private ProductDetails toDetails(Product product) {
    return new ProductDetails(product.getId(), product.getName(), product.getPrice(), product.getStock());
  }
}
