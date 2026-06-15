package pl.example.lab7.client;

import pl.example.lab7.domain.ProductView;

public interface ProductClient {
    ProductView getProduct(long productId);
    void reserve(long productId, int quantity);
}
