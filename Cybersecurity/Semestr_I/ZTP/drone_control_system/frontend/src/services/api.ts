// ─────────────────────────────────────────────────────────────────────────────
//  Typed API client – covers every REST endpoint exposed by the backend
// ─────────────────────────────────────────────────────────────────────────────

export const API_BASE = "http://localhost:8081/api/v1";

// ── Token storage ─────────────────────────────────────────────────────────────
const TOKEN_KEY = "drone_jwt";
export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY);
export const setToken = (t: string) => localStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

// ── Shared fetch helper ────────────────────────────────────────────────────────
async function req<T>(
  path: string,
  options: RequestInit = {},
  auth = true,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new ApiError(res.status, text);
  }
  if (res.status === 204 || res.headers.get("Content-Length") === "0") {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
//  TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export type Role = "ADMIN" | "OPERATOR" | "VIEWER";
export type DroneStatus = "IDLE" | "ACTIVE" | "IN_FLIGHT" | "MAINTENANCE";
export type MissionStatus = "PLANNED" | "ACTIVE" | "COMPLETED" | "ABORTED";
export type CommandType =
  | "ARM"
  | "DISARM"
  | "TAKEOFF"
  | "LAND"
  | "RTL"
  | "GOTO_WAYPOINT";
export type CommandStatus = "PENDING" | "ACKNOWLEDGED" | "REJECTED";

export interface AuthResponse {
  token: string;
  tokenType: string;
  expiresInMs: number;
  username: string;
  role: Role;
}

export interface Drone {
  id: string;
  name: string;
  model: string;
  serialNumber: string;
  status: DroneStatus;
  lastSeen: string | null;
}

export interface MissionResponse {
  id: string;
  name: string;
  status: MissionStatus;
  droneIds: string[];
}

export interface CommandResponse {
  commandId: string;
  droneId: string;
  type: CommandType;
  status: CommandStatus;
  acceptedAt: string;
}

export interface CommandAck {
  commandId: string;
  droneId: string;
  accepted: boolean;
  detail: string;
  timestamp: string;
}

export interface TelemetryResponse {
  droneId: string;
  timestamp: string;
  latitude: number;
  longitude: number;
  altitudeMeters: number;
  speedMetersPerSecond: number;
  headingDegrees: number;
  batteryPercentage: number;
  satellites: number;
  flightMode: string;
  armed: boolean;
}

export interface TelemetryPage {
  content: TelemetryResponse[];
  totalElements: number;
  totalPages: number;
  number: number;
  size: number;
}

export interface DroneState {
  droneId: string;
  lastUpdated: string;
  latest: TelemetryResponse;
}

// ═══════════════════════════════════════════════════════════════════════════════
//  AUTH
// ═══════════════════════════════════════════════════════════════════════════════

export const authApi = {
  login: (username: string, password: string) =>
    req<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }, false),

  register: (username: string, email: string, password: string) =>
    req<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password }),
    }, false),

  me: () => req<{ username: string; role: Role }>("/auth/me"),
};

// ═══════════════════════════════════════════════════════════════════════════════
//  DRONES
// ═══════════════════════════════════════════════════════════════════════════════

export const dronesApi = {
  getAll: () => req<Drone[]>("/drones"),
  getById: (id: string) => req<Drone>(`/drones/${id}`),
  create: (drone: Partial<Drone>) =>
    req<Drone>("/drones", { method: "POST", body: JSON.stringify(drone) }),
  updateStatus: (id: string, status: DroneStatus) =>
    req<Drone>(`/drones/${id}/status?status=${status}`, { method: "PATCH" }),
  delete: (id: string) =>
    req<void>(`/drones/${id}`, { method: "DELETE" }),
};

// ═══════════════════════════════════════════════════════════════════════════════
//  DRONE STATES (Live snapshot from Redis)
// ═══════════════════════════════════════════════════════════════════════════════

export const stateApi = {
  getAll: () => req<DroneState[]>("/drones/state"),
  getOne: (droneId: string) => req<DroneState>(`/drones/state/${droneId}`),
};

// ═══════════════════════════════════════════════════════════════════════════════
//  MISSIONS
// ═══════════════════════════════════════════════════════════════════════════════

export const missionsApi = {
  getAll: () => req<MissionResponse[]>("/missions"),
  getById: (id: string) => req<MissionResponse>(`/missions/${id}`),
  create: (name: string) =>
    req<MissionResponse>("/missions", {
      method: "POST",
      body: JSON.stringify({ name }),
    }),
  assignDrone: (missionId: string, droneId: string) =>
    req<void>(`/missions/${missionId}/drones/${droneId}`, { method: "POST" }),
  start: (id: string) =>
    req<MissionResponse>(`/missions/${id}/start`, { method: "POST" }),
  stop: (id: string) =>
    req<MissionResponse>(`/missions/${id}/stop`, { method: "POST" }),
  delete: (id: string) =>
    req<void>(`/missions/${id}`, { method: "DELETE" }),
};

// ═══════════════════════════════════════════════════════════════════════════════
//  COMMANDS
// ═══════════════════════════════════════════════════════════════════════════════

export interface CommandRequest {
  droneId: string;
  type: CommandType;
  altitudeMeters?: number;
  latitude?: number;
  longitude?: number;
}

export const commandsApi = {
  submit: (request: CommandRequest) =>
    req<CommandResponse>("/commands", {
      method: "POST",
      body: JSON.stringify(request),
    }),
  takeoff: (droneId: string, altitudeMeters: number) =>
    req<CommandResponse>(
      `/commands/${droneId}/takeoff?altitudeMeters=${altitudeMeters}`,
      { method: "POST" },
    ),
  land: (droneId: string) =>
    req<CommandResponse>(`/commands/${droneId}/land`, { method: "POST" }),
  rtl: (droneId: string) =>
    req<CommandResponse>(`/commands/${droneId}/rtl`, { method: "POST" }),
  waypoint: (
    droneId: string,
    latitude: number,
    longitude: number,
    altitudeMeters: number,
  ) =>
    req<CommandResponse>(
      `/commands/${droneId}/waypoint?latitude=${latitude}&longitude=${longitude}&altitudeMeters=${altitudeMeters}`,
      { method: "POST" },
    ),
  getQueue: (droneId: string) =>
    req<string[]>(`/commands/${droneId}/queue`),
  getStatus: (commandId: string) =>
    req<CommandStatus>(`/commands/status/${commandId}`),
};

// ═══════════════════════════════════════════════════════════════════════════════
//  TELEMETRY
// ═══════════════════════════════════════════════════════════════════════════════

export const telemetryApi = {
  getRecent: (droneId: string) =>
    req<TelemetryResponse[]>(`/telemetry/${droneId}/recent`),
  getHistory: (
    droneId: string,
    from?: string,
    to?: string,
    page = 0,
    size = 500,
  ) => {
    const params = new URLSearchParams({ page: String(page), size: String(size) });
    if (from) params.set("from", from);
    if (to) params.set("to", to);
    return req<TelemetryPage>(`/telemetry/${droneId}/history?${params}`);
  },
};
