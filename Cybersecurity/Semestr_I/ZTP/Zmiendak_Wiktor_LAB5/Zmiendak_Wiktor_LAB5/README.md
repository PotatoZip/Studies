# Lab 5 — Broker wiadomości (symulacja in-memory)

Ten lab realizuje temat: **brokerzy wiadomości** (pub/sub, routing key, asynchroniczność)
bez Dockera i bez zewnętrznych usług. Wykorzystujemy **InMemoryMessageBroker**.

## Uruchomienie
- `mvn test`
- lub uruchom aplikację: `mvn spring-boot:run`

Aplikacja domyślnie działa na `http://localhost:8080`.

## Endpointy
- `POST /orders` — tworzy zamówienie i publikuje event `orders.created`
- `GET /notifications/events` — lista odebranych eventów (po stronie "konsumenta")

## Wskazówka
### Zadania (w 100% weryfikowane testami)

#### Ocena 3.0
1. **Broker**: routowanie po `routingKey` + fan-out do wielu subskrybentów.
2. **Broker**: dostarczanie asynchroniczne (publish nie blokuje się na handlerze).
3. **Publisher**: publikuje `OrderCreatedEvent` na routingKey `orders.created`.
4. **OrderService**: po utworzeniu zamówienia wywołuje `publisher.publishOrderCreated(...)`.
5. **Listener**: subskrybuje `orders.created` i zapisuje event do `ReceivedEventsStore`.
6. **E2E**: `POST /orders` powoduje pojawienie się eventu na `GET /notifications/events`.

#### Ocena 4.0
7. **Idempotencja**: duplikat eventu (ten sam `eventId`) nie zwiększa liczby zapisów.
8. **Idempotencja**: wiele różnych `eventId` zapisuje się jako wiele wpisów.
9. **Odporność**: `eventId=null` jest ignorowany.
10. **Odporność**: duplikaty publikowane równolegle nadal dają tylko 1 zapis.

#### Ocena 5.0
`ANALIZA.md` (1–2 strony): omówienie brokera, routingu, asynchroniczności i idempotencji.

### Testy
Możesz uruchamiać zestawy:
- tylko 3.0: `mvn -Dtest=Grade3* test`
- tylko 4.0: `mvn -Dtest=Grade4* test`
- wszystko: `mvn test`

Pliki testów:
- 3.0: `Grade3BrokerRoutingTest`, `Grade3BrokerAsyncTest`, `Grade3PublisherRoutingKeyTest`,
  `Grade3OrderServicePublishesEventTest`, `Grade3ListenerConsumesEventTest`, `Grade3PublishAndConsumeTest`
- 4.0: `Grade4IdempotencyTest`, `Grade4MultipleDistinctEventsTest`, `Grade4NullEventIdIgnoredTest`,
  `Grade4ConcurrentDuplicateDeliveryTest`
