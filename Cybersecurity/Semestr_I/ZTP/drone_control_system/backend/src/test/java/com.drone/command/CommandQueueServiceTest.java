package com.drone.command;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class CommandQueueServiceTest {

    private CommandQueueService queue;

    @BeforeEach
    void setUp() {
        queue = new CommandQueueService();
    }

    private PendingCommand pending(String id, String drone) {
        return new PendingCommand(id, "req-" + id, drone, CommandType.TAKEOFF, "operator1");
    }

    @Test
    void enqueueTracksCommandAndOutstandingQueue() {
        queue.enqueue(pending("c1", "drone-1"));

        assertThat(queue.find("c1")).isPresent();
        assertThat(queue.find("c1").get().getStatus()).isEqualTo(CommandStatus.QUEUED);
        assertThat(queue.outstandingFor("drone-1")).containsExactly("c1");
    }

    @Test
    void outstandingPreservesSubmissionOrder() {
        queue.enqueue(pending("c1", "drone-1"));
        queue.enqueue(pending("c2", "drone-1"));
        queue.enqueue(pending("c3", "drone-1"));

        assertThat(queue.outstandingFor("drone-1")).containsExactly("c1", "c2", "c3");
    }

    @Test
    void updateStatusMutatesPendingCommand() {
        queue.enqueue(pending("c1", "drone-1"));

        queue.updateStatus("c1", CommandStatus.SENT);

        assertThat(queue.find("c1").get().getStatus()).isEqualTo(CommandStatus.SENT);
    }

    @Test
    void resolveSetsStatusAndRemovesFromQueue() {
        queue.enqueue(pending("c1", "drone-1"));
        queue.enqueue(pending("c2", "drone-1"));

        Optional<PendingCommand> resolved = queue.resolve("c1", CommandStatus.ACKNOWLEDGED);

        assertThat(resolved).isPresent();
        assertThat(resolved.get().getStatus()).isEqualTo(CommandStatus.ACKNOWLEDGED);
        assertThat(queue.outstandingFor("drone-1")).containsExactly("c2");
    }

    @Test
    void resolveUnknownCommandReturnsEmpty() {
        assertThat(queue.resolve("missing", CommandStatus.ACKNOWLEDGED)).isEmpty();
    }

    @Test
    void outstandingForUnknownDroneIsEmpty() {
        assertThat(queue.outstandingFor("ghost")).isEmpty();
    }
}
