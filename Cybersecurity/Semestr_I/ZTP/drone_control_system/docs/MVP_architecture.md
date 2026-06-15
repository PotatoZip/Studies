flowchart LR

%% =========================
%% STYLES
%% =========================
classDef front fill:#3498db,stroke:#2980b9,color:white,stroke-width:2px;
classDef back fill:#2980b9,stroke:#1a5276,color:white,stroke-width:2px;
classDef realtime fill:#9b59b6,stroke:#7e3f98,color:white,stroke-width:2px;
classDef broker fill:#8e44ad,stroke:#6b2c81,color:white,stroke-width:2px;
classDef mav fill:#8e44ad,stroke:#6b2c81,color:white,stroke-width:2px;
classDef drone fill:#34495e,stroke:#2c3e50,color:white,stroke-width:2px;
classDef storage fill:#34495e,stroke:#2c3e50,color:white,stroke-width:2px;

%% =========================
%% FRONTEND
%% =========================
subgraph FE[Frontend]
    direction LR
    UI[React GCS UI]:::front
end

%% =========================
%% CORE BACKEND (Simplified)
%% =========================
subgraph BE[Spring Boot Core]
    direction LR
    API[REST API & Auth]:::back
    WS[WebSocket Gateway]:::back
    CMD[Command Router]:::back
end

%% =========================
%% REALTIME & MESSAGING
%% =========================
subgraph RT[Realtime & State]
    direction LR
    BROKER[(MQTT Broker / Redis PubSub)]:::broker
    CACHE[(Redis Latest State)]:::realtime
end

%% =========================
%% MAVLINK LAYER
%% =========================
subgraph MAV[MAVLink Layer]
    direction LR
    ADAPTER[MAVLink Adapter]:::mav
    LINK[Local WiFi / Radio Link]:::mav
end

%% =========================
%% DRONE (MVP)
%% =========================
subgraph DRONE[Vehicle]
    direction LR
    FCU[Flight Controller PX4/ArduPilot]:::drone
end

%% =========================
%% STORAGE
%% =========================
subgraph DB[Storage]
    direction LR
    PG[(PostgreSQL Core)]:::storage
end

%% =========================
%% CONNECTIONS
%% =========================

UI -->|HTTPS REST| API
UI <-->|WebSocket| WS

%% Command Flow
API --> CMD
CMD -->|Commands| BROKER
BROKER -->|Commands| ADAPTER
ADAPTER -->|MAVLink| LINK
LINK <--> FCU

%% Acknowledgment Loop
ADAPTER -->|ACK Events| BROKER
BROKER -->|ACKs| CMD
CMD -->|Push ACK| WS

%% Telemetry Flow
FCU -->|Telemetry| LINK
LINK --> ADAPTER
ADAPTER -->|Raw Messages| BROKER

BROKER -->|Telemetry Updates| WS
BROKER -->|Update State| CACHE

%% Storage
API --> PG
