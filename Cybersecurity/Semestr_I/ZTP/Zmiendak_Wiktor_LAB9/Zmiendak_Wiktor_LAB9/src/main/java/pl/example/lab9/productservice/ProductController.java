package pl.example.lab9.productservice;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pl.example.lab9.contracts.ProductDetails;
import pl.example.lab9.contracts.ReserveProductCommand;
import pl.example.lab9.productservice.dto.CreateProductRequest;

import java.util.List;

@RestController
@RequestMapping("/product-service/products")
public class ProductController {

  private final ProductService productService;

  public ProductController(ProductService productService) {
    this.productService = productService;
  }

  @PostMapping
  public ResponseEntity<ProductDetails> createProduct(@Valid @RequestBody CreateProductRequest request) {
    ProductDetails created = productService.createProduct(request);
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
  }

  @GetMapping("/{id}")
  public ProductDetails getProduct(@PathVariable long id) {
    return productService.getProduct(id);
  }

  @GetMapping
  public List<ProductDetails> getProducts() {
    return productService.getProducts();
  }

  @PostMapping("/{id}/reservations")
  public ProductDetails reserveProduct(@PathVariable long id,
                                       @Valid @RequestBody ReserveProductCommand command) {
    return productService.reserveProduct(id, command.getQuantity());
  }
}
