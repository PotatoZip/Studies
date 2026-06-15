package com.drone.command;

import com.drone.command.dto.CommandRequest;
import com.drone.command.dto.CommandResponse;
import jakarta.validation.Valid;
import java.security.Principal;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Command endpoints (Epic 4.3). All require authentication; the issuing
 * operator is taken from the JWT principal so acknowledgements can be routed
 * back to that specific client over WebSocket.
 *
 * <p>{@link #submit} is the generic entry point; the typed helpers
 * (takeoff/land/rtl/waypoint) are thin conveniences over it.
 */
@RestController
@RequestMapping("/api/v1/commands")
@RequiredArgsConstructor
public class CommandController {

    private final CommandService commandService;
    private final CommandQueueService queueService;

    @PostMapping
    public ResponseEntity<CommandResponse> submit(@Valid @RequestBody CommandRequest request,
                                                  Principal principal) {
        CommandResponse response = commandService.submit(request, principal.getName());
        return ResponseEntity.accepted().body(response);
    }

    @PostMapping("/{droneId}/takeoff")
    public ResponseEntity<CommandResponse> takeoff(@PathVariable String droneId,
                                                   @RequestParam double altitudeMeters,
                                                   Principal principal) {
        return submitTyped(droneId, CommandType.TAKEOFF, altitudeMeters, null, null, principal);
    }

    @PostMapping("/{droneId}/land")
    public ResponseEntity<CommandResponse> land(@PathVariable String droneId, Principal principal) {
        return submitTyped(droneId, CommandType.LAND, null, null, null, principal);
    }

    @PostMapping("/{droneId}/rtl")
    public ResponseEntity<CommandResponse> rtl(@PathVariable String droneId, Principal principal) {
        return submitTyped(droneId, CommandType.RTL, null, null, null, principal);
    }

    @PostMapping("/{droneId}/waypoint")
    public ResponseEntity<CommandResponse> waypoint(@PathVariable String droneId,
                                                    @RequestParam double latitude,
                                                    @RequestParam double longitude,
                                                    @RequestParam double altitudeMeters,
                                                    Principal principal) {
        return submitTyped(droneId, CommandType.GOTO_WAYPOINT,
                altitudeMeters, latitude, longitude, principal);
    }

    /** Outstanding (unacknowledged) command IDs for a drone, in submission order. */
    @GetMapping("/{droneId}/queue")
    public List<String> queue(@PathVariable String droneId) {
        return queueService.outstandingFor(droneId);
    }

    /** Current status of a single command. */
    @GetMapping("/status/{commandId}")
    public ResponseEntity<CommandStatus> status(@PathVariable String commandId) {
        return queueService.find(commandId)
                .map(pc -> ResponseEntity.ok(pc.getStatus()))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND).build());
    }

    private ResponseEntity<CommandResponse> submitTyped(String droneId, CommandType type,
                                                        Double altitude, Double lat, Double lon,
                                                        Principal principal) {
        CommandRequest request = new CommandRequest();
        request.setDroneId(droneId);
        request.setType(type);
        request.setAltitudeMeters(altitude);
        request.setLatitude(lat);
        request.setLongitude(lon);
        return ResponseEntity.accepted().body(commandService.submit(request, principal.getName()));
    }
}
