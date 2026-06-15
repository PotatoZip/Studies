package pl.example.lab5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import pl.example.lab5.dto.CreateOrderRequest;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.model.Order;
import pl.example.lab5.service.OrderEventPublisher;
import pl.example.lab5.service.OrderService;
import pl.example.lab5.store.OrderStore;
import pl.example.lab5.store.ProductCatalog;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class Grade3OrderServicePublishesEventTest {

  @Test
  @DisplayName("3.0: OrderService tworzy OrderCreatedEvent i wywołuje publisher.publishOrderCreated")
  void orderServiceShouldCallPublisherWithCorrectEvent() {
    ProductCatalog catalog = new ProductCatalog();
    catalog.init(); // @PostConstruct in prod

    OrderStore orderStore = new OrderStore();

    OrderEventPublisher publisher = mock(OrderEventPublisher.class);
    OrderService service = new OrderService(catalog, orderStore, publisher);

    CreateOrderRequest req = new CreateOrderRequest();
    req.setProductId(1L);
    req.setQuantity(2);

    Order order = service.create(req);

    assertEquals(1L, order.getId());
    assertEquals(240.0, order.getTotal());

    ArgumentCaptor<OrderCreatedEvent> captor = ArgumentCaptor.forClass(OrderCreatedEvent.class);
    verify(publisher, times(1)).publishOrderCreated(captor.capture());

    OrderCreatedEvent event = captor.getValue();
    assertNotNull(event.getEventId(), "eventId should be generated");
    assertEquals(order.getId(), event.getOrderId());
    assertEquals(order.getProductId(), event.getProductId());
    assertEquals(order.getQuantity(), event.getQuantity());
    assertEquals(order.getTotal(), event.getTotal());
  }
}
