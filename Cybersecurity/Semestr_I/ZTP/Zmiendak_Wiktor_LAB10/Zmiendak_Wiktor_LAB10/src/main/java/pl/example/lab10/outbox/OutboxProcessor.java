package pl.example.lab10.outbox;

import org.springframework.stereotype.Component;
import pl.example.lab10.broker.MessageBroker;

import java.time.Clock;
import java.time.Instant;
import java.util.List;

@Component
public class OutboxProcessor {

  private final OutboxStore outboxStore;
  private final MessageBroker messageBroker;
  private final Clock clock;

  public OutboxProcessor(OutboxStore outboxStore, MessageBroker messageBroker, Clock clock) {
    this.outboxStore = outboxStore;
    this.messageBroker = messageBroker;
    this.clock = clock;
  }

  public int processPending() {
    List<OutboxEvent> pending = outboxStore.findUnprocessed();
    int published = 0;

    for (OutboxEvent event : pending) {
      messageBroker.publish(event.getRoutingKey(), event.getPayload());
      event.markProcessed(Instant.now(clock));
      published++;
    }

    return published;
  }
}
