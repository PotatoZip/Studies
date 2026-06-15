flowchart LR

%% =========================
%% STYLES
%% =========================
classDef front fill:#3498db,stroke:#2980b9,color:white,stroke-width:2px;
classDef media fill:#3498db,stroke:#2980b9,color:white,stroke-width:2px;
classDef back fill:#2980b9,stroke:#1a5276,color:white,stroke-width:2px;
classDef realtime fill:#9b59b6,stroke:#7e3f98,color:white,stroke-width:2px;
classDef proc fill:#9b59b6,stroke:#7e3f98,color:white,stroke-width:2px;
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
%% API LAYER
%% =========================
subgraph BE[Spring Boot Backend]
    direction LR
    API[REST API Controller]:::back
    WS[WebSocket Gateway STOMP]:::back
    AUTH[Auth Service JWT OAuth2]:::back
    CMD[Command Service]:::back
    MIS[Mission Service]:::back
end

%% =========================
%% MEDIA LAYER (NEW)
%% =========================
subgraph VIDEO[Media Layer]
    direction LR
    MEDIA[WebRTC / RTSP Media Server]:::media
end

%% =========================
%% REALTIME & STATE
%% =========================
subgraph RT[Realtime Layer]
    direction LR
    TEL[Telemetry Service]:::realtime
    CACHE[(Redis Latest State Cache)]:::realtime
end

%% =========================
%% MESSAGE BROKER (UPDATED)
%% =========================
subgraph MB[Messaging]
    direction LR
    BROKER[(Kafka / MQTT Cluster)]:::broker
end

%% =========================
%% MAVLINK LAYER
%% =========================
subgraph MAV[MAVLink Layer]
    direction LR
    ADAPTER[MAVLink Adapter Service Java dronefleet]:::mav
    LINK[Cloud Gateway VPN / 5G]:::mav
end

%% =========================
%% DRONE / EDGE (UPDATED)
%% =========================
subgraph DRONE[Vehicle]
    direction LR
    CC[Companion Computer Pi / Jetson]:::drone
    FCU[Flight Controller PX4 / ArduPilot]:::drone
    CAM[Payload Camera]:::drone
end

%% =========================
%% STORAGE
%% =========================
subgraph DB[Storage]
    direction LR
    PG[(PostgreSQL Missions Users)]:::storage
    TS[(Time Series DB Telemetry)]:::storage
end

%% =========================
%% PROCESSING
%% =========================
subgraph PROC[Processing]
    direction LR
    P1[Telemetry Processor]:::proc
    P2[Anomaly Detection]:::proc
end

%% =========================
%% CONNECTIONS
%% =========================

UI -->|HTTPS REST| API
UI -->|WebSocket| WS
UI <-->|WebRTC Live Feed| MEDIA

API --> AUTH
API --> CMD
API --> MIS

WS --> TEL

%% Command Flow
CMD -->|Command Events| BROKER
BROKER -->|Commands| ADAPTER
ADAPTER -->|Encrypted MAVLink| LINK
LINK <-->|Cellular / LTE| CC
CC <-->|Serial / UART| FCU

%% Command Acknowledgment Loop (NEW)
ADAPTER -->|ACK Events| BROKER
BROKER -->|ACKs| CMD
CMD -->|Push ACK| WS

%% Telemetry Flow
FCU -->|Telemetry| CC
CC --> LINK
LINK --> ADAPTER
ADAPTER -->|Raw Messages| BROKER

BROKER -->|Telemetry Events| TEL
TEL --> CACHE
TEL -->|Push Updates| WS

%% Video Flow (NEW)
CAM -->|Raw Video| CC
CC -->|RTSP / SRT Stream| MEDIA

%% Storage
MIS --> PG

%% Processing (UPDATED)
BROKER --> P1
P1 --> CACHE
P1 -->|Batch Normalized Telemetry| TS
P1 --> P2
