package pl.example.lab10.saga;

import org.springframework.stereotype.Component;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class ProcessedEventsStore {

  private final Set<String> processedEventIds = ConcurrentHashMap.newKeySet();

  public boolean tryMarkProcessed(String eventId) {
    if (eventId == null || eventId.isBlank()) {
      return false;
    }
    return processedEventIds.add(eventId);
  }

  public int count() {
    return processedEventIds.size();
  }
}
