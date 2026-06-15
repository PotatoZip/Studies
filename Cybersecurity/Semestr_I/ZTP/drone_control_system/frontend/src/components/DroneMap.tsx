import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ZoomIn, ZoomOut, Maximize, Navigation } from "lucide-react";

const DroneMap = () => {
  return (
    <Card className="relative h-full overflow-hidden">
      {/* Map Controls */}
      <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
        <Button size="sm" variant="secondary" className="h-8 w-8 p-0">
          <ZoomIn className="h-3 w-3" />
        </Button>
        <Button size="sm" variant="secondary" className="h-8 w-8 p-0">
          <ZoomOut className="h-3 w-3" />
        </Button>
        <Button size="sm" variant="secondary" className="h-8 w-8 p-0">
          <Maximize className="h-3 w-3" />
        </Button>
      </div>

      {/* Status Overlay */}
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
        <Badge variant="default" className="bg-primary text-primary-foreground">
          AUTONOMOUS MODE
        </Badge>
        <Badge variant="outline" className="bg-card">
          GPS: 38.9072° N, 77.0369° W
        </Badge>
      </div>

      {/* Map Container */}
      <div className="w-full h-full bg-gradient-to-br from-blue-50 to-blue-100 relative">
        {/* Placeholder Map Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-green-100 via-blue-50 to-blue-100">
          {/* Grid overlay for map-like appearance */}
          <div className="absolute inset-0 opacity-20">
            <div className="grid grid-cols-20 grid-rows-20 h-full w-full">
              {Array.from({ length: 400 }).map((_, i) => (
                <div key={i} className="border border-gray-300/30"></div>
              ))}
            </div>
          </div>

          {/* Simulated map features */}
          <div className="absolute top-1/3 left-1/4 w-20 h-8 bg-green-200 rounded opacity-60"></div>
          <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-gray-200 rounded opacity-60"></div>
          <div className="absolute bottom-1/4 left-1/3 w-32 h-4 bg-blue-200 rounded opacity-60"></div>

          {/* Drone Icon */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div className="relative">
              {/* Drone body */}
              <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center shadow-lg">
                <Navigation className="h-3 w-3 text-primary-foreground rotate-45" />
              </div>
              {/* Drone range circle */}
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 border-2 border-primary/30 rounded-full animate-pulse"></div>
            </div>
          </div>

          {/* Flight path */}
          <svg className="absolute inset-0 w-full h-full">
            <path
              d="M 20% 80% Q 40% 20% 60% 50% T 80% 30%"
              stroke="hsl(var(--primary))"
              strokeWidth="2"
              strokeDasharray="5,5"
              fill="none"
              opacity="0.6"
            />
          </svg>
        </div>

        {/* Map attribution */}
        <div className="absolute bottom-2 right-2 text-xs text-muted-foreground bg-card/80 px-2 py-1 rounded">
          Map Placeholder
        </div>
      </div>
    </Card>
  );
};

export default DroneMap;
