UAV Ground Control Station

Breakdown aligns with the classic client-server architecture, using a React-based web client and a Spring Boot server acting as the central Ground Control Station (GCS).

Epic 1: Infrastructure & Environment Setup

Task 1.1: Initialize Spring Boot core project (REST, WebSockets, Data JPA, Security).

Task 1.2: Initialize React web application (e.g., using Vite, TailwindCSS, State Management).

Task 1.3: Create Docker Compose configuration for local development (PostgreSQL, Redis, MQTT Broker/RabbitMQ).

Task 1.4: Setup basic CI/CD pipelines for linting and building both Client and Server.

Epic 2: Authentication & User Management

Task 2.1: [Backend] Design user database schema and create PostgreSQL entities.

Task 2.2: [Backend] Implement JWT-based registration and login REST API.

Task 2.3: [Frontend] Build Login and Registration UI views.

Task 2.4: [Frontend] Implement auth state management, token storage, and protected route wrappers.

Epic 3: MAVLink Adapter & Real-time Messaging

Task 3.1: [Adapter] Develop MAVLink connection layer (UDP/TCP) to interface with PX4/ArduPilot flight controllers.

Task 3.2: [Adapter] Implement telemetry parser translating raw MAVLink packets to internal JSON/DTO formats.

Task 3.3: [Adapter] Configure publishing of parsed telemetry data to the message broker (MQTT/Redis).

Task 3.4: [Adapter] Implement command listener subscribing to the broker and translating platform commands into MAVLink packets.

Task 3.5: [Adapter] Implement command Acknowledgement (ACK) extraction and publish back to the broker.

Epic 4: Ground Station Core Backend (Spring Boot)

Task 4.1: [Backend] Implement WebSocket Gateway with session authentication.

Task 4.2: [Backend] Develop Redis cache service to constantly maintain the "Latest State" of all connected drones.

Task 4.3: [Backend] Create Command Router logic: expose REST/WS endpoints for commands, validate them, and forward to the message broker.

Task 4.4: [Backend] Create Event Listener for ACKs from the broker and route them back to specific clients via WebSockets.

Task 4.5: [Backend] Implement Telemetry Persistence logic: batch and save flight telemetry data to PostgreSQL for mission history.

Task 4.6: [Backend] Expose REST API endpoints to fetch historical mission data for playback.

Epic 5: Ground Station Client (React Web App)

Task 5.1: [Frontend] Integrate a mapping library (e.g., Leaflet, Mapbox) for the primary operational view.

Task 5.2: [Frontend] Establish secure WebSocket connection and implement store/context to handle incoming telemetry streams.

Task 5.3: [Frontend] Build Multi-Drone Dashboard UI (list of active drones, basic status indicators like battery, GPS lock).

Task 5.4: [Frontend] Render drone markers and live movement paths on the map using incoming real-time telemetry.

Task 5.5: [Frontend] Develop Command Control Panel (UI buttons for Takeoff, Land, RTL, Waypoint generation) and link to API.

Task 5.6: [Frontend] Build Mission Playback UI (timeline slider, speed control) consuming the historical REST API.

Epic 6: Additional Features (Phase 2)

Task 6.1: [Backend] Implement an Anomaly Engine that monitors live telemetry streams against predefined safety thresholds.

Task 6.2: [Frontend] Build alert notification UI (toasts/modals) triggered by Anomaly Engine WebSocket events.

Task 6.3: [Adapter/Frontend] Set up WebRTC signaling server and client-side video player for drone camera feeds.
