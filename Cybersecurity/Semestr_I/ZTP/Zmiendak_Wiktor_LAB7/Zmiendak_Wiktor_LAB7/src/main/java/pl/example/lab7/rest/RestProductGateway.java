package pl.example.lab7.rest;

import pl.example.lab7.domain.ProductView;

public interface RestProductGateway {
    ProductView fetchProduct(long productId) throws RestNotFoundException;
    void reserve(long productId, int quantity) throws RestNotFoundException, RestConflictException;
}
