package pl.example.lab7.client;

import pl.example.lab7.domain.ProductView;
import pl.example.lab7.rest.RestConflictException;
import pl.example.lab7.rest.RestNotFoundException;
import pl.example.lab7.rest.RestProductGateway;

import java.util.Objects;
import java.util.NoSuchElementException;

public class RestProductClientAdapter implements ProductClient {

    private final RestProductGateway gateway;

    public RestProductClientAdapter(RestProductGateway gateway) {
        this.gateway = Objects.requireNonNull(gateway);
    }

    @Override
    public ProductView getProduct(long productId) {
        try {
            return gateway.fetchProduct(productId);
        } catch (RestNotFoundException e) {
            throw new NoSuchElementException("Product not found");
        }
    }

    @Override
    public void reserve(long productId, int quantity) {
        try {
            gateway.reserve(productId, quantity);
        } catch (RestNotFoundException e) {
            throw new NoSuchElementException("Product not found");
        } catch (RestConflictException e) {
            throw new IllegalStateException("Insufficient stock");
        }
    }
}
