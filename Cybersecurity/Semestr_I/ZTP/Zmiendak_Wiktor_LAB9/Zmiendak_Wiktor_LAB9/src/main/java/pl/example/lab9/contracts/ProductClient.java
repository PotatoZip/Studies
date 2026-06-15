package pl.example.lab9.contracts;

public interface ProductClient {

  ProductDetails getProduct(long productId);

  void reserveProduct(long productId, int quantity);
}
