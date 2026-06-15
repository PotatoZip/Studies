package pl.example.lab7.client;

import pl.example.lab7.domain.ProductView;
import pl.example.lab7.grpc.GrpcProductGateway;
import pl.example.lab7.grpc.GrpcStatusCode;
import pl.example.lab7.grpc.GrpcStatusException;

import java.util.Objects;
import java.util.NoSuchElementException;

public class GrpcProductClientAdapter implements ProductClient {

    private final GrpcProductGateway gateway;

    public GrpcProductClientAdapter(GrpcProductGateway gateway) {
        this.gateway = Objects.requireNonNull(gateway);
    }

    @Override
    public ProductView getProduct(long productId) {
        try {
            return gateway.getProduct(productId);
        } catch (GrpcStatusException e) {
            if (e.getCode() == GrpcStatusCode.NOT_FOUND) {
                throw new NoSuchElementException("Product not found");
            }
            throw e;
        }
    }

    @Override
    public void reserve(long productId, int quantity) {
        try {
            gateway.reserve(productId, quantity);
        } catch (GrpcStatusException e) {
            if (e.getCode() == GrpcStatusCode.NOT_FOUND) {
                throw new NoSuchElementException("Product not found");
            }
            if (e.getCode() == GrpcStatusCode.FAILED_PRECONDITION) {
                throw new IllegalStateException("Insufficient stock");
            }
            throw e;
        }
    }
}
