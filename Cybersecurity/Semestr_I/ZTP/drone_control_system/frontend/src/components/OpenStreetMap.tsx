import { useEffect, useState, useRef, useCallback } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Layers, Target, Maximize, Minimize } from "lucide-react";
import { wsService } from "@/services/websocket";
import { commandsApi } from "@/services/api";
import type { TelemetryResponse } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

// Fix default Leaflet icon paths broken by Vite bundling
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
// @ts-expect-error – Leaflet internal
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({ iconUrl: markerIcon, iconRetinaUrl: markerIcon2x, shadowUrl: markerShadow });

// ─── Icon factories ──────────────────────────────────────────────────────────

function makeDroneIcon(color: string, heading: number) {
  const svg = `
    <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"
         style="transform: rotate(${heading}deg);">
      <circle cx="16" cy="16" r="14" fill="${color}" fill-opacity="0.9" stroke="white" stroke-width="2"/>
      <polygon points="16,4 20,22 16,18 12,22" fill="white"/>
    </svg>`;
  return L.divIcon({
    className: "",
    html: svg,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -18],
  });
}

const DRONE_COLORS = [
  "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4",
];

// ─── Map re-center helper ────────────────────────────────────────────────────

function MapCenterHelper({ center }: { center: [number, number] | null }) {
  const map = useMap();
  const lastCenter = useRef<[number, number] | null>(null);
  useEffect(() => {
    if (!center) return;
    if (lastCenter.current && lastCenter.current[0] === center[0] && lastCenter.current[1] === center[1]) return;
    lastCenter.current = center;
    map.setView(center, map.getZoom(), { animate: true });
  }, [center, map]);
  return null;
}

// ─────────────────────────────────────────────────────────────────────────────

interface Props {
  selectedDroneId: string | null;
  onWaypointPlace?: (lat: number, lng: number) => void;
}

export default function DroneMap({ selectedDroneId, onWaypointPlace }: Props) {
  const { toast } = useToast();
  const [positionMap, setPositionMap] = useState<Map<string, TelemetryResponse>>(new Map());
  const [trailMap, setTrailMap] = useState<Map<string, Array<[number, number]>>>(new Map());
  const [droneIndex, setDroneIndex] = useState<Map<string, number>>(new Map());
  const [followSelected, setFollowSelected] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [waypointMode, setWaypointMode] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const colorCounter = useRef(0);

  // Subscribe to all-drones telemetry stream
  useEffect(() => {
    const unsub = wsService.onAllTelemetry((t: TelemetryResponse) => {
      if (t.latitude === 0 && t.longitude === 0) return;

      setPositionMap((prev) => new Map(prev).set(t.droneId, t));

      setDroneIndex((prev) => {
        if (prev.has(t.droneId)) return prev;
        const next = new Map(prev);
        next.set(t.droneId, colorCounter.current % DRONE_COLORS.length);
        colorCounter.current++;
        return next;
      });

      setTrailMap((prev) => {
        const clone = new Map(prev);
        const trail = clone.get(t.droneId) ?? [];
        clone.set(t.droneId, [...trail, [t.latitude, t.longitude] as [number, number]].slice(-120));
        return clone;
      });
    });
    return unsub;
  }, []);

  // Center of selected drone
  const selectedPos = selectedDroneId ? positionMap.get(selectedDroneId) : null;
  const center: [number, number] | null =
    followSelected && selectedPos
      ? [selectedPos.latitude, selectedPos.longitude]
      : null;

  const handleMapClick = useCallback(
    (e: L.LeafletMouseEvent) => {
      if (!waypointMode || !selectedDroneId) return;
      const { lat, lng } = e.latlng;
      onWaypointPlace?.(lat, lng);
      commandsApi
        .waypoint(selectedDroneId, lat, lng, 80)
        .then(() => toast({ title: "Waypoint sent", description: `${lat.toFixed(5)}, ${lng.toFixed(5)}` }))
        .catch((err: Error) => toast({ title: "Waypoint failed", description: err.message, variant: "destructive" }));
      setWaypointMode(false);
    },
    [waypointMode, selectedDroneId, onWaypointPlace, toast],
  );

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen().catch(console.error);
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    const handler = () => setIsFullscreen(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", handler);
    return () => document.removeEventListener("fullscreenchange", handler);
  }, []);

  const defaultCenter: [number, number] = [51.1079, 17.0385]; // Wrocław

  return (
    <Card className="relative h-full overflow-hidden" ref={containerRef}>
      <MapContainer
        center={defaultCenter}
        zoom={14}
        className="w-full h-full z-0"
        style={{ minHeight: "400px" }}
        whenCreated={(map) => {
          map.on("click", handleMapClick as unknown as L.LeafletEventHandlerFn);
        }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {followSelected && center && <MapCenterHelper center={center} />}

        {/* Render each drone */}
        {Array.from(positionMap.entries()).map(([droneId, tele]) => {
          const colorIdx = droneIndex.get(droneId) ?? 0;
          const color = DRONE_COLORS[colorIdx];
          const trail = trailMap.get(droneId) ?? [];
          const isSelected = droneId === selectedDroneId;

          return (
            <div key={droneId}>
              {/* Flight trail */}
              {trail.length > 1 && (
                <Polyline
                  positions={trail}
                  pathOptions={{ color, weight: isSelected ? 2.5 : 1.5, opacity: isSelected ? 0.8 : 0.4, dashArray: isSelected ? undefined : "4 4" }}
                />
              )}
              {/* Drone marker */}
              <Marker
                position={[tele.latitude, tele.longitude]}
                icon={makeDroneIcon(isSelected ? color : color + "99", tele.headingDegrees)}
                zIndexOffset={isSelected ? 1000 : 0}
              >
                <Popup>
                  <div className="text-xs space-y-0.5">
                    <div className="font-semibold">{droneId}</div>
                    <div>Alt: {tele.altitudeMeters.toFixed(1)} m</div>
                    <div>Speed: {(tele.speedMetersPerSecond * 3.6).toFixed(1)} km/h</div>
                    <div>Battery: {tele.batteryPercentage.toFixed(0)}%</div>
                    <div>Mode: {tele.flightMode}</div>
                    <div>Sats: {tele.satellites}</div>
                  </div>
                </Popup>
              </Marker>
            </div>
          );
        })}
      </MapContainer>

      {/* Overlay controls */}
      <div className="absolute top-3 right-3 z-[1000] flex flex-col gap-2">
        <Button
          size="icon"
          variant={followSelected ? "default" : "secondary"}
          className="h-8 w-8"
          title="Follow selected drone"
          onClick={() => setFollowSelected((v) => !v)}
        >
          <Target className="h-4 w-4" />
        </Button>
        <Button
          size="icon"
          variant={waypointMode ? "destructive" : "secondary"}
          className="h-8 w-8"
          title={waypointMode ? "Cancel waypoint" : "Click to send waypoint"}
          onClick={() => setWaypointMode((v) => !v)}
          disabled={!selectedDroneId}
        >
          <Layers className="h-4 w-4" />
        </Button>
        <Button
          size="icon"
          variant="secondary"
          className="h-8 w-8"
          onClick={toggleFullscreen}
          title="Fullscreen"
        >
          {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
        </Button>
      </div>

      {/* Status bar */}
      <div className="absolute bottom-3 left-3 z-[1000] flex gap-2">
        <Badge variant="secondary" className="text-[10px]">
          {positionMap.size} online
        </Badge>
        {waypointMode && (
          <Badge className="bg-yellow-500/90 text-black text-[10px] animate-pulse">
            Click map to send waypoint
          </Badge>
        )}
      </div>
    </Card>
  );
}
