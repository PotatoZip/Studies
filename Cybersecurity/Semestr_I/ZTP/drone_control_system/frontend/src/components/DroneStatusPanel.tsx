import { useEffect, useState, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import {
  Battery,
  Signal,
  Gauge,
  Navigation,
  Satellite,
  Compass,
  Activity,
  Wifi,
  WifiOff,
  ChevronRight,
  RefreshCw,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  ResponsiveContainer,
} from "recharts";
import { dronesApi, stateApi } from "@/services/api";
import type { Drone, DroneState, TelemetryResponse } from "@/services/api";
import { wsService } from "@/services/websocket";
import { useQuery } from "@tanstack/react-query";

// ─────────────────────────────────────────────────────────────────────────────

interface Props {
  selectedDroneId: string | null;
  onSelectDrone: (id: string) => void;
}

const STATUS_COLOR: Record<string, string> = {
  IDLE: "bg-muted text-muted-foreground",
  ACTIVE: "bg-blue-500/20 text-blue-400",
  IN_FLIGHT: "bg-success/20 text-green-400",
  MAINTENANCE: "bg-yellow-500/20 text-yellow-400",
};

const BATTERY_COLOR = (pct: number) => {
  if (pct > 60) return "text-green-400";
  if (pct > 30) return "text-yellow-400";
  return "text-red-400";
};

function formatHms(seconds: number) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return h > 0
    ? `${h}h ${m}m`
    : `${m}m ${String(s).padStart(2, "0")}s`;
}

// ─────────────────────────────────────────────────────────────────────────────

export default function DroneStatusPanel({ selectedDroneId, onSelectDrone }: Props) {
  // Fleet list from REST
  const { data: drones = [], refetch: refetchDrones } = useQuery({
    queryKey: ["drones"],
    queryFn: dronesApi.getAll,
    refetchInterval: 15_000,
  });

  // Live states from Redis via REST (bootstraps before WS kicks in)
  const { data: states = [] } = useQuery({
    queryKey: ["droneStates"],
    queryFn: stateApi.getAll,
    refetchInterval: 5_000,
  });

  // Live telemetry map { droneId → latest TelemetryResponse }
  const [telemetryMap, setTelemetryMap] = useState<Map<string, TelemetryResponse>>(new Map());

  // Speed/altitude history for mini-chart { droneId → [{time, speed, altitude}] }
  const [historyMap, setHistoryMap] = useState<Map<string, Array<{ time: string; speed: number; altitude: number }>>>(new Map());

  const [wsConnected, setWsConnected] = useState(wsService.isConnected);

  // Seed initial telemetry map from REST states
  useEffect(() => {
    if (states.length === 0) return;
    setTelemetryMap((prev) => {
      const next = new Map(prev);
      for (const s of states) {
        if (s.latest && !next.has(s.droneId)) {
          next.set(s.droneId, s.latest);
        }
      }
      return next;
    });
  }, [states]);

  // WebSocket subscription – fan-in all drones
  useEffect(() => {
    const unsub = wsService.onAllTelemetry((t) => {
      setWsConnected(true);
      setTelemetryMap((prev) => new Map(prev).set(t.droneId, t));
      setHistoryMap((prev) => {
        const clone = new Map(prev);
        const entry = clone.get(t.droneId) ?? [];
        const ts = new Date(t.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
        const next = [...entry, { time: ts, speed: +(t.speedMetersPerSecond * 3.6).toFixed(1), altitude: +t.altitudeMeters.toFixed(1) }].slice(-30);
        clone.set(t.droneId, next);
        return clone;
      });
    });
    return unsub;
  }, []);

  // Auto-select first drone
  useEffect(() => {
    if (!selectedDroneId && drones.length > 0) {
      onSelectDrone(drones[0].id);
    }
  }, [drones, selectedDroneId, onSelectDrone]);

  const selected = drones.find((d) => d.id === selectedDroneId);
  const selectedTelemetry = selectedDroneId ? telemetryMap.get(selectedDroneId) : null;
  const selectedHistory = selectedDroneId ? historyMap.get(selectedDroneId) ?? [] : [];

  return (
    <div className="space-y-3 animate-fade-in">
      {/* Connection status */}
      <Card>
        <CardHeader className="pb-2 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center justify-between">
            <span className="flex items-center gap-2">
              {wsConnected ? <Wifi className="h-3.5 w-3.5 text-green-400" /> : <WifiOff className="h-3.5 w-3.5 text-red-400" />}
              Backend Connection
            </span>
            <button onClick={() => refetchDrones()} title="Refresh">
              <RefreshCw className="h-3 w-3 text-muted-foreground hover:text-foreground transition-colors" />
            </button>
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-4">
          <div className="flex gap-2">
            <Badge className={wsConnected ? "bg-green-500/20 text-green-400 border-green-500/30" : "bg-red-500/20 text-red-400 border-red-500/30"}>
              {wsConnected ? "WebSocket Live" : "WebSocket Offline"}
            </Badge>
            <Badge variant="secondary">{drones.length} drones</Badge>
          </div>
        </CardContent>
      </Card>

      {/* Fleet list */}
      <Card>
        <CardHeader className="pb-2 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center gap-2">
            <Activity className="h-3.5 w-3.5" /> Fleet
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-2 px-2 space-y-1">
          {drones.length === 0 && (
            <p className="text-xs text-muted-foreground px-2 py-2">No drones registered.</p>
          )}
          {drones.map((drone) => {
            const tele = telemetryMap.get(drone.id);
            const isOnline = !!tele;
            const isSelected = drone.id === selectedDroneId;
            return (
              <button
                key={drone.id}
                onClick={() => onSelectDrone(drone.id)}
                className={`w-full flex items-center gap-2 px-2 py-2 rounded-md text-left transition-colors ${isSelected ? "bg-primary/10 border border-primary/30" : "hover:bg-muted/50"}`}
              >
                <div className={`w-2 h-2 rounded-full shrink-0 ${isOnline ? "bg-green-400 animate-pulse" : "bg-gray-500"}`} />
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-medium truncate">{drone.name}</div>
                  <div className="text-[10px] text-muted-foreground truncate">{drone.model}</div>
                </div>
                <Badge className={`text-[10px] px-1.5 py-0 ${STATUS_COLOR[drone.status] ?? ""}`}>
                  {drone.status}
                </Badge>
                {isSelected && <ChevronRight className="h-3 w-3 shrink-0 text-primary" />}
              </button>
            );
          })}
        </CardContent>
      </Card>

      {/* Selected drone detail */}
      {selected && (
        <>
          <Card>
            <CardHeader className="pb-2 pt-3 px-4">
              <CardTitle className="text-xs font-medium flex items-center gap-2">
                <Navigation className="h-3.5 w-3.5 text-primary" />
                {selected.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="pb-3 px-4 space-y-2.5">
              {selectedTelemetry ? (
                <>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Gauge className="h-3.5 w-3.5 text-primary" />
                      <span className="text-xs">Speed</span>
                    </div>
                    <span className="text-xs font-semibold">
                      {(selectedTelemetry.speedMetersPerSecond * 3.6).toFixed(1)} km/h
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Navigation className="h-3.5 w-3.5 text-primary" />
                      <span className="text-xs">Altitude</span>
                    </div>
                    <span className="text-xs font-semibold">{selectedTelemetry.altitudeMeters.toFixed(1)} m</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Compass className="h-3.5 w-3.5 text-primary" />
                      <span className="text-xs">Heading</span>
                    </div>
                    <span className="text-xs font-semibold">{selectedTelemetry.headingDegrees.toFixed(0)}°</span>
                  </div>

                  <Separator />

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Battery className={`h-3.5 w-3.5 ${BATTERY_COLOR(selectedTelemetry.batteryPercentage)}`} />
                      <span className="text-xs">Battery</span>
                    </div>
                    <span className={`text-xs font-semibold ${BATTERY_COLOR(selectedTelemetry.batteryPercentage)}`}>
                      {selectedTelemetry.batteryPercentage.toFixed(0)}%
                    </span>
                  </div>
                  <Progress value={selectedTelemetry.batteryPercentage} className="h-1.5" />

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Satellite className="h-3.5 w-3.5 text-primary" />
                      <span className="text-xs">GPS Sats</span>
                    </div>
                    <span className="text-xs font-semibold">{selectedTelemetry.satellites}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Signal className="h-3.5 w-3.5 text-primary" />
                      <span className="text-xs">Flight Mode</span>
                    </div>
                    <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
                      {selectedTelemetry.flightMode}
                    </Badge>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Armed</span>
                    <Badge className={`text-[10px] px-1.5 py-0 ${selectedTelemetry.armed ? "bg-red-500/20 text-red-400" : "bg-muted text-muted-foreground"}`}>
                      {selectedTelemetry.armed ? "ARMED" : "DISARMED"}
                    </Badge>
                  </div>

                  <Separator />

                  <div className="flex items-center justify-between text-[10px] text-muted-foreground">
                    <span>Lat: {selectedTelemetry.latitude.toFixed(5)}</span>
                    <span>Lon: {selectedTelemetry.longitude.toFixed(5)}</span>
                  </div>
                </>
              ) : (
                <p className="text-xs text-muted-foreground">No live telemetry yet…</p>
              )}
            </CardContent>
          </Card>

          {/* Mini speed/altitude chart */}
          {selectedHistory.length > 1 && (
            <Card>
              <CardHeader className="pb-1 pt-3 px-4">
                <CardTitle className="text-xs font-medium">Live Speed (km/h)</CardTitle>
              </CardHeader>
              <CardContent className="pb-3 px-4">
                <div className="h-24">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={selectedHistory}>
                      <XAxis dataKey="time" hide />
                      <YAxis domain={["auto", "auto"]} hide />
                      <Line type="monotone" dataKey="speed" stroke="hsl(var(--primary))" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}

