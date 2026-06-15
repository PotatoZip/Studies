package pl.example.lab7;

import pl.example.lab7.client.GrpcProductClientAdapter;
import pl.example.lab7.client.RestProductClientAdapter;
import pl.example.lab7.domain.ProductView;
import pl.example.lab7.grpc.*;
import pl.example.lab7.rest.*;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade3AdaptersMappingTest {

    @Test
    void restAdapter_mapsNotFound_toNoSuchElement() {
        RestProductGateway gw = mock(RestProductGateway.class);
        when(gw.fetchProduct(123L)).thenThrow(new RestNotFoundException("404"));

        RestProductClientAdapter adapter = new RestProductClientAdapter(gw);
        NoSuchElementException ex = assertThrows(NoSuchElementException.class, () -> adapter.getProduct(123L));
        assertEquals("Product not found", ex.getMessage());
    }

    @Test
    void restAdapter_mapsConflict_toInsufficientStock() {
        RestProductGateway gw = mock(RestProductGateway.class);
        doThrow(new RestConflictException("409")).when(gw).reserve(1L, 2);

        RestProductClientAdapter adapter = new RestProductClientAdapter(gw);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> adapter.reserve(1L, 2));
        assertEquals("Insufficient stock", ex.getMessage());
    }

    @Test
    void grpcAdapter_mapsNotFound_toNoSuchElement() {
        GrpcProductGateway gw = mock(GrpcProductGateway.class);
        when(gw.getProduct(9L)).thenThrow(new GrpcStatusException(GrpcStatusCode.NOT_FOUND, "nf"));

        GrpcProductClientAdapter adapter = new GrpcProductClientAdapter(gw);
        NoSuchElementException ex = assertThrows(NoSuchElementException.class, () -> adapter.getProduct(9L));
        assertEquals("Product not found", ex.getMessage());
    }

    @Test
    void grpcAdapter_mapsFailedPrecondition_toInsufficientStock() {
        GrpcProductGateway gw = mock(GrpcProductGateway.class);
        doThrow(new GrpcStatusException(GrpcStatusCode.FAILED_PRECONDITION, "no stock")).when(gw).reserve(5L, 1);

        GrpcProductClientAdapter adapter = new GrpcProductClientAdapter(gw);
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> adapter.reserve(5L, 1));
        assertEquals("Insufficient stock", ex.getMessage());
    }

    @Test
    void adapters_passThroughSuccess() {
        ProductView pv = new ProductView(1L, "Keyboard", BigDecimal.valueOf(100), 10);

        RestProductGateway rest = mock(RestProductGateway.class);
        when(rest.fetchProduct(1L)).thenReturn(pv);
        RestProductClientAdapter restAdapter = new RestProductClientAdapter(rest);
        assertEquals(pv, restAdapter.getProduct(1L));

        GrpcProductGateway grpc = mock(GrpcProductGateway.class);
        when(grpc.getProduct(1L)).thenReturn(pv);
        GrpcProductClientAdapter grpcAdapter = new GrpcProductClientAdapter(grpc);
        assertEquals(pv, grpcAdapter.getProduct(1L));
    }
}
