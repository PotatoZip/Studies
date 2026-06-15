package pl.example.lab10;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab10.broker.MessageBroker;
import pl.example.lab10.order.OrderServiceImpl;
import pl.example.lab10.outbox.OutboxProcessor;
import pl.example.lab10.outbox.OutboxStore;
import pl.example.lab10.product.ProductCatalog;
import pl.example.lab10.saga.ProcessedEventsStore;
import pl.example.lab10.saga.StockReservationSaga;

import java.lang.reflect.Field;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class Grade3ArchitectureTest {

  @Test
  @DisplayName("OrderServiceImpl zapisuje do outboxa i nie publikuje eventów bezpośrednio")
  void orderServiceUsesOutboxButNotBroker() {
    assertHasField(OrderServiceImpl.class, OutboxStore.class);
    assertDoesNotHaveField(OrderServiceImpl.class, MessageBroker.class);
    assertDoesNotHaveField(OrderServiceImpl.class, ProductCatalog.class);
  }

  @Test
  @DisplayName("OutboxProcessor jest miejscem integracji outboxa z brokerem")
  void outboxProcessorConnectsOutboxWithBroker() {
    assertHasField(OutboxProcessor.class, OutboxStore.class);
    assertHasField(OutboxProcessor.class, MessageBroker.class);
  }

  @Test
  @DisplayName("Saga zna katalog produktów, brokera i store przetworzonych eventów")
  void sagaHasRequiredDependencies() {
    assertHasField(StockReservationSaga.class, ProductCatalog.class);
    assertHasField(StockReservationSaga.class, MessageBroker.class);
    assertHasField(StockReservationSaga.class, ProcessedEventsStore.class);
  }

  private static void assertHasField(Class<?> owner, Class<?> fieldType) {
    assertTrue(
        Arrays.stream(owner.getDeclaredFields()).map(Field::getType).anyMatch(fieldType::equals),
        owner.getSimpleName() + " should have field of type " + fieldType.getSimpleName()
    );
  }

  private static void assertDoesNotHaveField(Class<?> owner, Class<?> fieldType) {
    assertFalse(
        Arrays.stream(owner.getDeclaredFields()).map(Field::getType).anyMatch(fieldType::equals),
        owner.getSimpleName() + " should not have field of type " + fieldType.getSimpleName()
    );
  }
}
