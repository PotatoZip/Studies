package pl.example.lab10.product;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import pl.example.lab10.product.dto.CreateProductRequest;

import java.util.List;

@RestController
public class ProductController {

  private final ProductCatalog productCatalog;

  public ProductController(ProductCatalog productCatalog) {
    this.productCatalog = productCatalog;
  }

  @PostMapping("/products")
  public ResponseEntity<Product> createProduct(@Valid @RequestBody CreateProductRequest request) {
    Product product = productCatalog.create(request.getName(), request.getStock());
    return ResponseEntity.status(HttpStatus.CREATED).body(product);
  }

  @GetMapping("/products/{id}")
  public Product getProduct(@PathVariable long id) {
    return productCatalog.findById(id)
        .orElseThrow(() -> new ProductNotFoundException("Product not found"));
  }

  @GetMapping("/products")
  public List<Product> getProducts() {
    return productCatalog.findAll();
  }
}
