package pl.example.lab9.productservice;

import org.springframework.stereotype.Component;
import pl.example.lab9.contracts.ProductClient;
import pl.example.lab9.contracts.ProductDetails;

@Component
public class LocalProductClient implements ProductClient {

  private final ProductService productService;

  public LocalProductClient(ProductService productService) {
    this.productService = productService;
  }

  @Override
  public ProductDetails getProduct(long productId) {
    return productService.getProduct(productId);
  }

  @Override
  public void reserveProduct(long productId, int quantity) {
    productService.reserveProduct(productId, quantity);
  }
}
