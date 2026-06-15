package pl.example.lab7.client;

import pl.example.lab7.config.AppConfig;
import pl.example.lab7.grpc.GrpcProductGateway;
import pl.example.lab7.rest.RestProductGateway;

import java.util.Objects;

public class ProductClientFactory {

    private final RestProductGateway restGateway;
    private final GrpcProductGateway grpcGateway;

    public ProductClientFactory(RestProductGateway restGateway, GrpcProductGateway grpcGateway) {
        this.restGateway = Objects.requireNonNull(restGateway);
        this.grpcGateway = Objects.requireNonNull(grpcGateway);
    }

    public ProductClient create(AppConfig cfg) {
        ProductClient client;
        if (cfg.mode() == AppConfig.Mode.REST) {
            client = new RestProductClientAdapter(restGateway);
        } else if (cfg.mode() == AppConfig.Mode.GRPC) {
            client = new GrpcProductClientAdapter(grpcGateway);
        } else {
            throw new IllegalArgumentException("Unsupported mode: " + cfg.mode());
        }

        if (cfg.retryEnabled()) {
            client = new RetryingProductClient(client, cfg.maxAttempts());
        }
        if (cfg.cacheEnabled()) {
            client = new CachingProductClient(client);
        }
        return client;
    }
}
