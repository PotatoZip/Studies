package pl.example.lab7;

import pl.example.lab7.client.*;
import pl.example.lab7.config.AppConfig;
import pl.example.lab7.grpc.GrpcProductGateway;
import pl.example.lab7.rest.RestProductGateway;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade3FactorySelectionTest {

    @Test
    void factory_selectsRestAdapter() {
        RestProductGateway rest = mock(RestProductGateway.class);
        GrpcProductGateway grpc = mock(GrpcProductGateway.class);
        ProductClientFactory factory = new ProductClientFactory(rest, grpc);

        ProductClient client = factory.create(new AppConfig(AppConfig.Mode.REST, false, false, 3));
        assertTrue(client instanceof RestProductClientAdapter, "Expected RestProductClientAdapter");
    }

    @Test
    void factory_selectsGrpcAdapter() {
        RestProductGateway rest = mock(RestProductGateway.class);
        GrpcProductGateway grpc = mock(GrpcProductGateway.class);
        ProductClientFactory factory = new ProductClientFactory(rest, grpc);

        ProductClient client = factory.create(new AppConfig(AppConfig.Mode.GRPC, false, false, 3));
        assertTrue(client instanceof GrpcProductClientAdapter, "Expected GrpcProductClientAdapter");
    }
}
