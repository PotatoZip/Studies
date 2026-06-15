package pl.example.lab7.grpc;

import pl.example.lab7.domain.ProductView;

public interface GrpcProductGateway {
    ProductView getProduct(long productId) throws GrpcStatusException;
    void reserve(long productId, int quantity) throws GrpcStatusException;
}
