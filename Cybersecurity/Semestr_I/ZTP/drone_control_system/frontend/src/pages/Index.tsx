import { useState, useEffect } from "react";
import DroneStatusPanel from "@/components/DroneStatusPanel";
import MissionControls from "@/components/MissionControls";
import DroneMap from "@/components/OpenStreetMap";
import DroneAnalytics from "@/components/DroneAnalytics";
import ThemeToggle from "@/components/ThemeToggle";
import useDocumentTitle from "@/hooks/useDocumentTitle";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LogOut, User } from "lucide-react";

const Index = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [selectedDroneId, setSelectedDroneId] = useState<string | null>(null);
  const { user, logout } = useAuth();

  useDocumentTitle("Cosmo Drone Panel");

  useDocumentTitle("Cosmo Drone Panel");

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm transition-colors duration-300">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 bg-primary rounded-lg flex items-center justify-center animate-scale-in">
                <img src="/src/assets/logo.png" alt="Logo" className="w-9 h-9 rounded-lg" onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }} />
              </div>
              <div className="animate-fade-in">
                <h1 className="text-lg font-bold text-foreground leading-tight">Drone Control System</h1>
                <p className="text-xs text-muted-foreground">Autonomous Flight Management</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <ThemeToggle />
              <div className="text-right animate-fade-in hidden sm:block">
                <div className="text-sm font-medium tabular-nums">
                  {currentTime.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
                </div>
                <div className="text-xs text-muted-foreground">Local Time</div>
              </div>
              {user && (
                <div className="flex items-center gap-2">
                  <div className="hidden sm:flex items-center gap-1.5">
                    <User className="h-3.5 w-3.5 text-muted-foreground" />
                    <span className="text-xs font-medium">{user.username}</span>
                    <Badge variant="secondary" className="text-[10px] px-1.5 py-0">{user.role}</Badge>
                  </div>
                  <Button variant="ghost" size="icon" className="h-8 w-8" onClick={logout} title="Logout">
                    <LogOut className="h-3.5 w-3.5" />
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main layout */}
      <div className="container mx-auto px-4 py-3 h-[calc(100vh-72px)]">
        <div className="grid grid-cols-12 gap-3 h-full">
          {/* Left – fleet panel */}
          <div className="col-span-3 overflow-y-auto max-h-full">
            <DroneStatusPanel
              selectedDroneId={selectedDroneId}
              onSelectDrone={setSelectedDroneId}
            />
          </div>

          {/* Centre – live map */}
          <div className="col-span-6 h-full flex flex-col gap-3">
            <div className="flex-1 min-h-0">
              <DroneMap selectedDroneId={selectedDroneId} />
            </div>
          </div>

          {/* Right – controls + analytics */}
          <div className="col-span-3 overflow-y-auto max-h-full space-y-3">
            <MissionControls selectedDroneId={selectedDroneId} />
            <DroneAnalytics selectedDroneId={selectedDroneId} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;

