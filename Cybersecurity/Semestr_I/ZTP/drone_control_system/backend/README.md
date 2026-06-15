# Drone Control System — Backend (Ground Control Station)

Spring Boot 3.2 / Java 17 backend that acts as the central **Ground Control
Station (GCS)** coordinating multiple drones. It authenticates operators,
streams live telemetry to the React frontend over WebSocket, caches each drone's
latest state, routes validated commands to a (mocked) MAVLink adapter, and
persists telemetry for mission playback.

---

## Table of contents

- [Architecture](#architecture)
- [Module map](#module-map)
- [Data & message flow](#data--message-flow)
- [Configuration](#configuration)
- [Running locally](#running-locally)
- [REST API reference](#rest-api-reference)
- [WebSocket (STOMP) API](#websocket-stomp-api)
- [Testing](#testing)
- [Notes & conventions](#notes--conventions)

---

## Architecture

- **Stateless JWT security** guards REST and the STOMP CONNECT frame with the
  same token.
- A **`MessageBroker` abstraction** (Redis Pub/Sub implementation) decouples
  producers/consumers. Telemetry has three independent consumers — the
  WebSocket broadcaster, the Redis state cache, and the persistence buffer.
- The **MAVLink adapter is mocked**: interfaces are real; a simulator generates
  flight data and acknowledges commands, so the whole pipeline runs without
  hardware.

## Module map

All sources live under `src/main/java/com.drone/`.

| Package | Responsibility |
|---|---|
| `authentication` | User entity, JWT register/login, `UserDetails` |
| `security` | `JwtService`, `JwtAuthenticationFilter`, `JwtProperties` |
| `common.config` | Security, WebSocket (STOMP), Redis, Scheduling config |
| `common.exception` | `GlobalExceptionHandler`, `ApiError`, typed exceptions |
| `messaging` | `MessageBroker` interface, `BrokerChannels`, Redis impl |
| `websocket` | STOMP auth interceptor, telemetry + ack broadcasters |
| `state` | `DroneStateService` (Redis "Latest State", TTL) + controller |
| `command` | Command router: validation, queue, REST endpoints |
| `telemetry` | Batch persistence + recent/history REST API |
| `mavlink` | Connection / parser / translator interfaces + mocks + sim |
| `drone`, `mission` | Pre-existing CRUD for drone registry & missions |

## Data & message flow

**Telemetry (inbound):**
`MockMavlinkConnection` → `MavlinkTelemetryParser` → broker `gcs.telemetry` →
fanned out to (a) `TelemetryBroadcaster` → STOMP `/topic/telemetry/{droneId}`,
(b) `DroneStateService` → Redis `drone:state:{id}` (with TTL),
(c) `TelemetryIngestionListener` → `TelemetryBatchWriter` → PostgreSQL/H2.

**Command (outbound) + ack (inbound):**
REST `POST /commands` → `CommandValidator` → `CommandQueueService` (QUEUED) →
broker `gcs.commands` (SENT) → `MavlinkAdapterService` → `CommandTranslator` →
`MockMavlinkConnection.send` → mock emits `COMMAND_ACK` → broker `gcs.acks` →
`CommandAckBroadcaster` resolves the command (ACKNOWLEDGED/REJECTED) and pushes
it to the issuing operator's `/user/queue/acks`.

## Configuration

Properties (with defaults) — local profile in `application.properties`, Docker
profile in `application-docker.properties`:

| Property | Default | Purpose |
|---|---|---|
| `server.port` | `8081` | HTTP port |
| `spring.data.redis.host` / `.port` | `localhost` / `6379` | Redis (cache + broker) |
| `app.jwt.secret` | dev secret | HMAC signing key (≥256 bits). Override via `APP_JWT_SECRET` |
| `app.jwt.expiration-ms` | `86400000` | Token lifetime (24h) |
| `app.cors.allowed-origins` | `http://localhost:8080,...` | Allowed CORS / WS origins (CSV) |
| `app.state.ttl-seconds` | `30` | Latest-state expiry per drone |
| `app.telemetry.batch.max-size` | `200` | Flush when buffer reaches this size |
| `app.telemetry.batch.flush-interval-ms` | `2000` | Periodic flush cadence |
| `app.mavlink.simulation.enabled` | `true` | Toggle the mock data generator |
| `app.mavlink.simulation.drone-count` | `3` | Number of simulated drones |
| `app.mavlink.simulation.interval-ms` | `1000` | Telemetry emit interval |

Local dev uses **H2** (in-memory, `create-drop`); Docker uses **PostgreSQL**.
**Redis must be running** — the Pub/Sub listener container connects on startup.

## Running locally

```bash
# 1. Start Redis (required). Docker:
docker run -d --rm -p 6379:6379 redis:7-alpine
#    ...or the full stack:
docker compose up postgres redis

# 2. Run the backend (H2 + localhost Redis)
cd backend
mvn spring-boot:run

# 3. Smoke test
curl -s localhost:8081/api/v1/health
curl -s -X POST localhost:8081/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"operator1","email":"op1@example.com","password":"password123"}'
```

With simulation enabled, `GET /api/v1/drones/state` will show drones within a
second or two.

## REST API reference

Base path: `/api/v1`. All routes except `/auth/**` and `/health` require
`Authorization: Bearer <token>`.

### Auth (public)
| Method | Path | Body / params | Description |
|---|---|---|---|
| `POST` | `/auth/register` | `{username,email,password,role?}` | Create operator, returns JWT |
| `POST` | `/auth/login` | `{username,password}` | Authenticate, returns JWT |
| `GET` | `/auth/me` | – | Current principal |

### Drone state (live cache)
| Method | Path | Description |
|---|---|---|
| `GET` | `/drones/state` | All online drones (non-expired) |
| `GET` | `/drones/state/{droneId}` | One drone's latest state (404 if expired) |

### Commands
| Method | Path | Body / params | Description |
|---|---|---|---|
| `POST` | `/commands` | `{droneId,type,altitudeMeters?,latitude?,longitude?}` | Generic submit (202) |
| `POST` | `/commands/{droneId}/takeoff` | `?altitudeMeters=` | Convenience |
| `POST` | `/commands/{droneId}/land` | – | Convenience |
| `POST` | `/commands/{droneId}/rtl` | – | Convenience |
| `POST` | `/commands/{droneId}/waypoint` | `?latitude=&longitude=&altitudeMeters=` | Convenience |
| `GET` | `/commands/{droneId}/queue` | – | Outstanding command IDs |
| `GET` | `/commands/status/{commandId}` | – | Command status |

`type` ∈ `ARM, DISARM, TAKEOFF, LAND, RTL, GOTO_WAYPOINT`.

### Telemetry
| Method | Path | Params | Description |
|---|---|---|---|
| `POST` | `/telemetry/ingest` | body | Direct HTTP ingest (non-MAVLink) |
| `GET` | `/telemetry/{droneId}/recent` | – | Last 100 samples (newest first) |
| `GET` | `/telemetry/{droneId}/history` | `from,to` (ISO-8601), `page,size` | Paged history, ascending |

Errors use a uniform body: `{timestamp,status,error,message,path,fieldErrors?}`.

## WebSocket (STOMP) API

- **Handshake:** `GET /ws` (SockJS enabled).
- **Authenticate:** send the JWT as a native STOMP header on CONNECT:
  `Authorization: Bearer <token>`. Unauthenticated CONNECTs are rejected.
- **Subscribe:**
  - `/topic/telemetry/{droneId}` — telemetry for one drone
  - `/topic/telemetry` — all drones
  - `/user/queue/acks` — command acknowledgements for *your* commands

Example (stomp.js):

```js
const client = new Client({
  webSocketFactory: () => new SockJS('http://localhost:8081/ws'),
  connectHeaders: { Authorization: `Bearer ${token}` },
});
client.onConnect = () => {
  client.subscribe('/topic/telemetry', m => console.log(JSON.parse(m.body)));
  client.subscribe('/user/queue/acks', m => console.log('ACK', JSON.parse(m.body)));
};
client.activate();
```

## Testing

Unit tests (JUnit 5 + Mockito + AssertJ) cover the service-layer logic without
requiring Redis or a database:

```bash
cd backend
mvn test
```

Covered: JWT issue/validate, auth register/login, command validation/routing/
queue, Redis state service (mocked template), telemetry batch writer & mapping,
MAVLink command translation & telemetry parsing, and the mock simulator.

## Notes & conventions

- **Source layout:** sources sit under a single directory literally named
  `com.drone/`. Package declarations are standard (`com.drone.x.y`) and
  `mvn compile` is the source of truth — some IDEs mis-report package errors
  for this layout.
- **Messaging is swappable:** implement `MessageBroker` (e.g. MQTT) and the rest
  of the backend is unaffected.
- **MAVLink is mocked:** replace `MockMavlinkConnection` with a real UDP/TCP
  implementation of `MavlinkConnection`; parser/translator interfaces stay.
