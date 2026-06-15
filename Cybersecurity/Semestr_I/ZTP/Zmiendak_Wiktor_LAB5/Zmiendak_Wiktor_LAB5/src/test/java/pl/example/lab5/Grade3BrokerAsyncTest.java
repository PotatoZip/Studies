package pl.example.lab5;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import pl.example.lab5.broker.InMemoryMessageBroker;

import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;

class Grade3BrokerAsyncTest {

  @Test
  @DisplayName("3.0: Broker dostarcza wiadomości asynchronicznie (publish nie blokuje się na handlerze)")
  void publishShouldBeAsync() throws Exception {
    InMemoryMessageBroker broker = new InMemoryMessageBroker();

    CountDownLatch handlerStarted = new CountDownLatch(1);
    CountDownLatch allowHandlerToFinish = new CountDownLatch(1);

    broker.subscribe("rk", msg -> {
      handlerStarted.countDown();
      try {
        // blokujemy handler, żeby sprawdzić czy publish nie czeka synchronicznie
        allowHandlerToFinish.await(2, TimeUnit.SECONDS);
      } catch (InterruptedException ignored) {
        Thread.currentThread().interrupt();
      }
    });

    ExecutorService es = Executors.newSingleThreadExecutor(r -> {
      Thread t = new Thread(r);
      t.setDaemon(true);
      t.setName("test-publish-thread");
      return t;
    });

    Future<?> f = es.submit(() -> broker.publish("rk", "x"));

    try {
      // jeśli publish jest synchroniczny, Future nie skończy się dopóki nie odblokujemy handlera
      f.get(250, TimeUnit.MILLISECONDS);
      assertTrue(handlerStarted.await(500, TimeUnit.MILLISECONDS), "Expected handler to start");
    } catch (TimeoutException te) {
      fail("publish() seems to be synchronous (it blocked waiting for handler)");
    } finally {
      allowHandlerToFinish.countDown();
      es.shutdownNow();
    }
  }
}
