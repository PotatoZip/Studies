import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Play, Square, Home, ArrowDown, Plane, Map, Plus,
  Trash2, CheckCircle2, XCircle, Clock, Loader2,
} from "lucide-react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { missionsApi, commandsApi, dronesApi } from "@/services/api";
import type { MissionResponse, CommandAck } from "@/services/api";
import { wsService } from "@/services/websocket";

interface Props { selectedDroneId: string | null; }

const MISSION_STATUS_COLOR: Record<string, string> = {
  PLANNED: "bg-blue-500/20 text-blue-400",
  ACTIVE: "bg-green-500/20 text-green-400",
  COMPLETED: "bg-muted text-muted-foreground",
  ABORTED: "bg-red-500/20 text-red-400",
};

export default function MissionControls({ selectedDroneId }: Props) {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const [takeoffAlt, setTakeoffAlt] = useState("50");
  const [waypointLat, setWaypointLat] = useState("");
  const [waypointLon, setWaypointLon] = useState("");
  const [waypointAlt, setWaypointAlt] = useState("80");
  const [newMissionName, setNewMissionName] = useState("");
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [assignDialogOpen, setAssignDialogOpen] = useState(false);
  const [assignMissionId, setAssignMissionId] = useState("");
  const [cmdLog, setCmdLog] = useState<CommandAck[]>([]);

  const { data: missions = [], isLoading: missionsLoading } = useQuery({
    queryKey: ["missions"],
    queryFn: missionsApi.getAll,
    refetchInterval: 10_000,
  });

  const { data: drones = [] } = useQuery({ queryKey: ["drones"], queryFn: dronesApi.getAll });

  const createMission = useMutation({
    mutationFn: (name: string) => missionsApi.create(name),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ["missions"] }); setNewMissionName(""); setCreateDialogOpen(false); toast({ title: "Mission created" }); },
    onError: (e: Error) => toast({ title: "Error", description: e.message, variant: "destructive" }),
  });

  const startMission = useMutation({
    mutationFn: missionsApi.start,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["missions"] }),
    onError: (e: Error) => toast({ title: "Error", description: e.message, variant: "destructive" }),
  });

  const stopMission = useMutation({
    mutationFn: missionsApi.stop,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["missions"] }),
    onError: (e: Error) => toast({ title: "Error", description: e.message, variant: "destructive" }),
  });

  const deleteMission = useMutation({
    mutationFn: missionsApi.delete,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["missions"] }),
    onError: (e: Error) => toast({ title: "Error", description: e.message, variant: "destructive" }),
  });

  const assignDrone = useMutation({
    mutationFn: ({ missionId, droneId }: { missionId: string; droneId: string }) =>
      missionsApi.assignDrone(missionId, droneId),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ["missions"] }); setAssignDialogOpen(false); toast({ title: "Drone assigned" }); },
    onError: (e: Error) => toast({ title: "Error", description: e.message, variant: "destructive" }),
  });

  const sendCommand = useCallback(async (fn: () => Promise<unknown>, label: string) => {
    if (!selectedDroneId) { toast({ title: "No drone selected", variant: "destructive" }); return; }
    try { await fn(); toast({ title: `${label} sent` }); }
    catch (e) { toast({ title: "Command failed", description: (e as Error).message, variant: "destructive" }); }
  }, [selectedDroneId, toast]);

  useEffect(() => {
    const unsub = wsService.onAck((ack) => {
      setCmdLog((prev) => [ack, ...prev].slice(0, 20));
      ack.accepted
        ? toast({ title: "Command ACK", description: ack.detail ?? "OK" })
        : toast({ title: "Command REJECTED", description: ack.detail, variant: "destructive" });
    });
    return unsub;
  }, [toast]);

  return (
    <div className="space-y-3">
      {/* Flight Commands */}
      <Card>
        <CardHeader className="pb-2 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center gap-2">
            <Plane className="h-3.5 w-3.5" /> Flight Commands
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-4 space-y-3">
          {!selectedDroneId && <p className="text-xs text-muted-foreground">Select a drone first.</p>}
          <div className="flex items-end gap-2">
            <div className="flex-1">
              <Label className="text-[10px] text-muted-foreground">Takeoff Alt (m)</Label>
              <Input type="number" value={takeoffAlt} onChange={(e) => setTakeoffAlt(e.target.value)} className="h-7 text-xs" min={5} max={500} />
            </div>
            <Button size="sm" className="h-7 text-xs" disabled={!selectedDroneId}
              onClick={() => sendCommand(() => commandsApi.takeoff(selectedDroneId!, parseFloat(takeoffAlt)), "Takeoff")}>
              <Play className="h-3 w-3 mr-1" /> Takeoff
            </Button>
          </div>
          <div className="grid grid-cols-3 gap-1.5">
            <Button variant="outline" size="sm" className="h-7 text-xs" disabled={!selectedDroneId}
              onClick={() => sendCommand(() => commandsApi.land(selectedDroneId!), "Land")}>
              <ArrowDown className="h-3 w-3 mr-1" /> Land
            </Button>
            <Button variant="outline" size="sm" className="h-7 text-xs" disabled={!selectedDroneId}
              onClick={() => sendCommand(() => commandsApi.rtl(selectedDroneId!), "RTL")}>
              <Home className="h-3 w-3 mr-1" /> RTL
            </Button>
            <Button variant="secondary" size="sm" className="h-7 text-xs" disabled={!selectedDroneId}
              onClick={() => sendCommand(() => commandsApi.submit({ droneId: selectedDroneId!, type: "ARM" }), "Arm")}>
              ARM
            </Button>
          </div>
          <Separator />
          <div>
            <Label className="text-[10px] text-muted-foreground uppercase tracking-wide">
              <Map className="h-3 w-3 inline mr-1" />Goto Waypoint
            </Label>
            <div className="grid grid-cols-3 gap-1.5 mt-1">
              <div><Label className="text-[10px]">Lat</Label><Input type="number" step="0.0001" value={waypointLat} onChange={(e) => setWaypointLat(e.target.value)} className="h-7 text-xs" placeholder="51.107" /></div>
              <div><Label className="text-[10px]">Lon</Label><Input type="number" step="0.0001" value={waypointLon} onChange={(e) => setWaypointLon(e.target.value)} className="h-7 text-xs" placeholder="17.038" /></div>
              <div><Label className="text-[10px]">Alt (m)</Label><Input type="number" value={waypointAlt} onChange={(e) => setWaypointAlt(e.target.value)} className="h-7 text-xs" /></div>
            </div>
            <Button size="sm" variant="secondary" className="w-full h-7 text-xs mt-2"
              disabled={!selectedDroneId || !waypointLat || !waypointLon}
              onClick={() => sendCommand(() => commandsApi.waypoint(selectedDroneId!, parseFloat(waypointLat), parseFloat(waypointLon), parseFloat(waypointAlt)), "Waypoint")}>
              Send Waypoint
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Missions */}
      <Card>
        <CardHeader className="pb-2 pt-3 px-4">
          <CardTitle className="text-xs font-medium flex items-center justify-between">
            <span className="flex items-center gap-2"><Map className="h-3.5 w-3.5" /> Missions</span>
            <div className="flex gap-1">
              <Dialog open={assignDialogOpen} onOpenChange={setAssignDialogOpen}>
                <DialogTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-6 w-6" title="Assign drone"><Plane className="h-3 w-3" /></Button>
                </DialogTrigger>
                <DialogContent className="max-w-xs">
                  <DialogHeader><DialogTitle>Assign Drone to Mission</DialogTitle></DialogHeader>
                  <div className="space-y-3">
                    <div>
                      <Label className="text-xs">Mission</Label>
                      <Select onValueChange={setAssignMissionId}>
                        <SelectTrigger className="h-8"><SelectValue placeholder="Select mission" /></SelectTrigger>
                        <SelectContent>{missions.map((m) => <SelectItem key={m.id} value={m.id}>{m.name}</SelectItem>)}</SelectContent>
                      </Select>
                    </div>
                    <Button size="sm" className="w-full" disabled={!assignMissionId || !selectedDroneId}
                      onClick={() => assignDrone.mutate({ missionId: assignMissionId, droneId: selectedDroneId! })}>Assign</Button>
                  </div>
                </DialogContent>
              </Dialog>
              <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
                <DialogTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-6 w-6" title="New mission"><Plus className="h-3 w-3" /></Button>
                </DialogTrigger>
                <DialogContent className="max-w-xs">
                  <DialogHeader><DialogTitle>New Mission</DialogTitle></DialogHeader>
                  <div className="space-y-3">
                    <Input placeholder="Mission name" value={newMissionName} onChange={(e) => setNewMissionName(e.target.value)} />
                    <Button size="sm" className="w-full" disabled={!newMissionName.trim() || createMission.isPending}
                      onClick={() => createMission.mutate(newMissionName.trim())}>
                      {createMission.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : "Create"}
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="pb-3 px-3 space-y-1.5">
          {missionsLoading && <p className="text-xs text-muted-foreground px-1">Loading…</p>}
          {!missionsLoading && missions.length === 0 && <p className="text-xs text-muted-foreground px-1">No missions yet.</p>}
          {missions.map((mission) => (
            <div key={mission.id} className="flex items-center gap-1.5 px-1 py-1.5 rounded-md hover:bg-muted/50">
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium truncate">{mission.name}</div>
                <div className="flex items-center gap-1 mt-0.5">
                  <Badge className={`text-[9px] px-1 py-0 ${MISSION_STATUS_COLOR[mission.status] ?? ""}`}>{mission.status}</Badge>
                  <span className="text-[9px] text-muted-foreground">{mission.droneIds.length} drone(s)</span>
                </div>
              </div>
              <div className="flex gap-0.5">
                {mission.status === "PLANNED" && (
                  <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => startMission.mutate(mission.id)}><Play className="h-3 w-3 text-green-400" /></Button>
                )}
                {mission.status === "ACTIVE" && (
                  <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => stopMission.mutate(mission.id)}><Square className="h-3 w-3 text-red-400" /></Button>
                )}
                <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => deleteMission.mutate(mission.id)}><Trash2 className="h-3 w-3 text-muted-foreground hover:text-red-400" /></Button>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Command log */}
      {cmdLog.length > 0 && (
        <Card>
          <CardHeader className="pb-2 pt-3 px-4">
            <CardTitle className="text-xs font-medium flex items-center gap-2"><Clock className="h-3.5 w-3.5" /> Command Log</CardTitle>
          </CardHeader>
          <CardContent className="pb-3 px-3 space-y-1">
            {cmdLog.map((ack, i) => (
              <div key={i} className="flex items-center gap-2 text-[10px]">
                {ack.accepted ? <CheckCircle2 className="h-3 w-3 text-green-400 shrink-0" /> : <XCircle className="h-3 w-3 text-red-400 shrink-0" />}
                <span className="text-muted-foreground font-mono">{ack.commandId.slice(0, 8)}</span>
                <span className="truncate">{ack.detail ?? (ack.accepted ? "OK" : "Rejected")}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
