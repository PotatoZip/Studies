package pl.example.lab5.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import pl.example.lab5.events.OrderCreatedEvent;
import pl.example.lab5.store.ReceivedEventsStore;

import java.util.List;

@RestController
public class NotificationsController {

  private final ReceivedEventsStore store;

  public NotificationsController(ReceivedEventsStore store) {
    this.store = store;
  }

  @GetMapping("/notifications/events")
  public List<OrderCreatedEvent> events() {
    return store.getEvents();
  }
}
