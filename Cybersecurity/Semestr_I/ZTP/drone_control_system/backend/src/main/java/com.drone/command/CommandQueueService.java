package com.drone.command;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Queue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * Command queue management (Epic 4.3). Tracks every command awaiting an ack and
 * maintains a per-drone FIFO queue of outstanding command IDs. Backed by
 * concurrent collections so the REST thread (enqueue) and the broker listener
 * thread (ack) can operate safely in parallel.
 */
@Slf4j
@Service
public class CommandQueueService {

    private final Map<String, PendingCommand> pendingById = new ConcurrentHashMap<>();
    private final Map<String, Queue<String>> queueByDrone = new ConcurrentHashMap<>();

    /** Register a newly accepted command in QUEUED state. */
    public void enqueue(PendingCommand command) {
        pendingById.put(command.getCommandId(), command);
        queueByDrone
                .computeIfAbsent(command.getDroneId(), d -> new ConcurrentLinkedQueue<>())
                .add(command.getCommandId());
        log.debug("Queued command {} ({}) for drone {}",
                command.getCommandId(), command.getType(), command.getDroneId());
    }

    public void updateStatus(String commandId, CommandStatus status) {
        PendingCommand command = pendingById.get(commandId);
        if (command != null) {
            command.setStatus(status);
        }
    }

    public Optional<PendingCommand> find(String commandId) {
        return Optional.ofNullable(pendingById.get(commandId));
    }

    /**
     * Resolve a command against an ack: update its status and remove it from the
     * drone's outstanding queue. Returns the command if it was still pending.
     */
    public Optional<PendingCommand> resolve(String commandId, CommandStatus status) {
        PendingCommand command = pendingById.get(commandId);
        if (command == null) {
            return Optional.empty();
        }
        command.setStatus(status);
        Queue<String> queue = queueByDrone.get(command.getDroneId());
        if (queue != null) {
            queue.remove(commandId);
        }
        return Optional.of(command);
    }

    /** Command IDs still outstanding for a drone, in submission order. */
    public List<String> outstandingFor(String droneId) {
        Queue<String> queue = queueByDrone.get(droneId);
        return queue == null ? List.of() : List.copyOf(queue);
    }
}
