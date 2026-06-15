package pl.example.lab5.store;

import org.springframework.stereotype.Component;
import pl.example.lab5.events.OrderCreatedEvent;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

@Component
public class ReceivedEventsStore {

  private final Set<String> seenEventIds = ConcurrentHashMap.newKeySet();
  private final List<OrderCreatedEvent> events = new CopyOnWriteArrayList<>();

  /**
   * Dodaje event tylko jeśli eventId nie był jeszcze widziany (idempotencja).
   */
  public boolean addIfFirstTime(OrderCreatedEvent e) {
    if (e == null || e.getEventId() == null || e.getEventId().isBlank())
      return false;
    boolean first = seenEventIds.add(e.getEventId());
    if (first)
      events.add(e);
    return first;
  }

  public List<OrderCreatedEvent> getEvents() {
    return List.copyOf(events);
  }

  public int size() {
    return events.size();
  }

  public void clear() {
    seenEventIds.clear();
    events.clear();
  }
}
