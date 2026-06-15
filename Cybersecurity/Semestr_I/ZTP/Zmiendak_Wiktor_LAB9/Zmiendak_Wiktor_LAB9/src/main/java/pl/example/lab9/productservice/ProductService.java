package pl.example.lab9.productservice;

import pl.example.lab9.contracts.ProductDetails;
import pl.example.lab9.productservice.dto.CreateProductRequest;

import java.util.List;

public interface ProductService {

  ProductDetails createProduct(CreateProductRequest request);

  ProductDetails getProduct(long id);

  List<ProductDetails> getProducts();

  ProductDetails reserveProduct(long id, int quantity);
}
