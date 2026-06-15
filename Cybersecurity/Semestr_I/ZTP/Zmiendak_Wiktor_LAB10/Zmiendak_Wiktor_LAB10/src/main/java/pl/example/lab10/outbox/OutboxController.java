package pl.example.lab10.outbox;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
public class OutboxController {

  private final OutboxStore outboxStore;
  private final OutboxProcessor outboxProcessor;

  public OutboxController(OutboxStore outboxStore, OutboxProcessor outboxProcessor) {
    this.outboxStore = outboxStore;
    this.outboxProcessor = outboxProcessor;
  }

  @PostMapping("/outbox/process")
  public Map<String, Integer> processOutbox() {
    return Map.of("processed", outboxProcessor.processPending());
  }

  @GetMapping("/outbox/events")
  public List<OutboxEvent> getOutboxEvents() {
    return outboxStore.findAll();
  }
}
