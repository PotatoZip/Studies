package pl.example.lab7;

import pl.example.lab7.client.*;
import pl.example.lab7.config.AppConfig;
import pl.example.lab7.grpc.GrpcProductGateway;
import pl.example.lab7.rest.RestProductGateway;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade4FactoryPipelineTest {

    @Test
    void factory_wrapsAsCachingRetryingAdapter_inThatOrder() {
        RestProductGateway rest = mock(RestProductGateway.class);
        GrpcProductGateway grpc = mock(GrpcProductGateway.class);
        ProductClientFactory factory = new ProductClientFactory(rest, grpc);

        ProductClient client = factory.create(new AppConfig(AppConfig.Mode.REST, true, true, 3));

        assertTrue(client instanceof CachingProductClient);
        ProductClient d1 = ((CachingProductClient) client).delegate();
        assertTrue(d1 instanceof RetryingProductClient);
        ProductClient d2 = ((RetryingProductClient) d1).delegate();
        assertTrue(d2 instanceof RestProductClientAdapter);
    }
}
