import { Client, type IMessage } from "@stomp/stompjs";
import SockJS from "sockjs-client";
import type { TelemetryResponse, CommandAck } from "./api";

// ─────────────────────────────────────────────────────────────────────────────
//  Singleton STOMP-over-SockJS service
//  Connects to ws://localhost:8081/ws with the JWT from localStorage.
//
//  Usage:
//    wsService.connect(token)
//    const unsub = wsService.onTelemetry(droneId, cb)   // per-drone
//    const unsub = wsService.onAllTelemetry(cb)          // fleet feed
//    const unsub = wsService.onAck(cb)                   // command acks
//    wsService.disconnect()
// ─────────────────────────────────────────────────────────────────────────────

type TelemetryCb = (t: TelemetryResponse) => void;
type AckCb = (a: CommandAck) => void;
type Unsubscribe = () => void;

class WebSocketService {
  private client: Client | null = null;
  private connected = false;
  private pendingSubscriptions: Array<() => void> = [];

  // listener registries
  private telemetryListeners: Map<string, Set<TelemetryCb>> = new Map();
  private allTelemetryListeners: Set<TelemetryCb> = new Set();
  private ackListeners: Set<AckCb> = new Set();

  connect(token: string): Promise<void> {
    if (this.client?.active) return Promise.resolve();

    return new Promise((resolve, reject) => {
      this.client = new Client({
        webSocketFactory: () =>
          new SockJS("http://localhost:8081/ws") as WebSocket,
        connectHeaders: {
          Authorization: `Bearer ${token}`,
        },
        reconnectDelay: 5000,
        onConnect: () => {
          this.connected = true;
          this.registerCoreSubscriptions();
          // run any subscriptions queued before connect
          this.pendingSubscriptions.forEach((fn) => fn());
          this.pendingSubscriptions = [];
          resolve();
        },
        onStompError: (frame) => {
          console.error("STOMP error", frame);
          reject(new Error(frame.headers["message"] ?? "STOMP error"));
        },
        onDisconnect: () => {
          this.connected = false;
        },
      });
      this.client.activate();
    });
  }

  disconnect() {
    this.client?.deactivate();
    this.connected = false;
    this.telemetryListeners.clear();
    this.allTelemetryListeners.clear();
    this.ackListeners.clear();
  }

  get isConnected() {
    return this.connected;
  }

  // ── Core subscriptions (fleet-level + acks) ───────────────────────────────

  private registerCoreSubscriptions() {
    if (!this.client) return;

    // All-drones feed
    this.client.subscribe("/topic/telemetry", (msg: IMessage) => {
      try {
        const t: TelemetryResponse = JSON.parse(msg.body);
        this.allTelemetryListeners.forEach((cb) => cb(t));
        // also fan out to per-drone listeners
        this.telemetryListeners.get(t.droneId)?.forEach((cb) => cb(t));
      } catch {
        /* ignore malformed */
      }
    });

    // Command acks (per-user queue)
    this.client.subscribe("/user/queue/acks", (msg: IMessage) => {
      try {
        const ack: CommandAck = JSON.parse(msg.body);
        this.ackListeners.forEach((cb) => cb(ack));
      } catch {
        /* ignore */
      }
    });
  }

  // ── Public listener registration ──────────────────────────────────────────

  /** Subscribe to telemetry for a specific drone. */
  onTelemetry(droneId: string, cb: TelemetryCb): Unsubscribe {
    if (!this.telemetryListeners.has(droneId)) {
      this.telemetryListeners.set(droneId, new Set());
    }
    this.telemetryListeners.get(droneId)!.add(cb);
    return () => this.telemetryListeners.get(droneId)?.delete(cb);
  }

  /** Subscribe to the merged all-drones telemetry stream. */
  onAllTelemetry(cb: TelemetryCb): Unsubscribe {
    this.allTelemetryListeners.add(cb);
    return () => this.allTelemetryListeners.delete(cb);
  }

  /** Subscribe to command acknowledgements. */
  onAck(cb: AckCb): Unsubscribe {
    this.ackListeners.add(cb);
    return () => this.ackListeners.delete(cb);
  }
}

// Export singleton
export const wsService = new WebSocketService();
