import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";
import { TrendingUp, Battery, Navigation2, Satellite } from "lucide-react";
import { wsService } from "@/services/websocket";
import type { TelemetryResponse } from "@/services/api";
import { useQuery } from "@tanstack/react-query";
import { telemetryApi } from "@/services/api";

interface Props { selectedDroneId: string | null; }

interface Point { time: string; speed: number; altitude: number; battery: number; satellites: number; }

const TOOLTIP_STYLE = {
  backgroundColor: "hsl(var(--card))",
  border: "1px solid hsl(var(--border))",
  borderRadius: "6px",
  fontSize: "11px",
};

export default function DroneAnalytics({ selectedDroneId }: Props) {
  const [history, setHistory] = useState<Point[]>([]);

  // Bootstrap from REST recent telemetry
  const { data: recent = [] } = useQuery({
    queryKey: ["telemetry-recent", selectedDroneId],
    queryFn: () => telemetryApi.getRecent(selectedDroneId!),
    enabled: !!selectedDroneId,
    staleTime: 5_000,
  });

  useEffect(() => {
    if (!recent.length) return;
    const pts: Point[] = [...recent].reverse().slice(-60).map((t) => ({
      time: new Date(t.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }),
      speed: +(t.speedMetersPerSecond * 3.6).toFixed(1),
      altitude: +t.altitudeMeters.toFixed(1),
      battery: +t.batteryPercentage.toFixed(1),
      satellites: t.satellites,
    }));
    setHistory(pts);
  }, [recent]);

  // Live WebSocket updates
  useEffect(() => {
    if (!selectedDroneId) return;
    const unsub = wsService.onTelemetry(selectedDroneId, (t: TelemetryResponse) => {
      const ts = new Date(t.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      setHistory((prev) => [
        ...prev,
        {
          time: ts,
          speed: +(t.speedMetersPerSecond * 3.6).toFixed(1),
          altitude: +t.altitudeMeters.toFixed(1),
          battery: +t.batteryPercentage.toFixed(1),
          satellites: t.satellites,
        },
      ].slice(-60));
    });
    return unsub;
  }, [selectedDroneId]);

  if (!selectedDroneId) {
    return (
      <Card>
        <CardContent className="py-8 text-center text-xs text-muted-foreground">
          Select a drone to see analytics.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {/* Speed */}
      <Card>
        <CardHeader className="pb-1 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center gap-2">
            <TrendingUp className="h-3.5 w-3.5 text-primary" /> Speed (km/h)
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-3">
          <div className="h-28">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="time" fontSize={9} stroke="hsl(var(--muted-foreground))" tick={false} />
                <YAxis fontSize={9} stroke="hsl(var(--muted-foreground))" domain={["auto", "auto"]} width={28} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Line type="monotone" dataKey="speed" stroke="hsl(var(--primary))" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Altitude */}
      <Card>
        <CardHeader className="pb-1 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center gap-2">
            <Navigation2 className="h-3.5 w-3.5 text-blue-400" /> Altitude (m)
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-3">
          <div className="h-28">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="time" fontSize={9} stroke="hsl(var(--muted-foreground))" tick={false} />
                <YAxis fontSize={9} stroke="hsl(var(--muted-foreground))" domain={["auto", "auto"]} width={28} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Area type="monotone" dataKey="altitude" stroke="hsl(217 91% 60%)" fill="hsl(217 91% 60% / 0.15)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Battery */}
      <Card>
        <CardHeader className="pb-1 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center gap-2">
            <Battery className="h-3.5 w-3.5 text-green-400" /> Battery (%)
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-3">
          <div className="h-28">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="time" fontSize={9} stroke="hsl(var(--muted-foreground))" tick={false} />
                <YAxis fontSize={9} stroke="hsl(var(--muted-foreground))" domain={[0, 100]} width={28} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Area type="monotone" dataKey="battery" stroke="hsl(142 71% 45%)" fill="hsl(142 71% 45% / 0.15)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* GPS Satellites */}
      <Card>
        <CardHeader className="pb-1 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center gap-2">
            <Satellite className="h-3.5 w-3.5 text-yellow-400" /> GPS Satellites
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-3">
          <div className="h-24">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <XAxis dataKey="time" fontSize={9} tick={false} />
                <YAxis fontSize={9} domain={[0, 20]} width={22} />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Line type="stepAfter" dataKey="satellites" stroke="hsl(48 96% 53%)" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
