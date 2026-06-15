package com.drone.telemetry.repository;

import com.drone.telemetry.model.TelemetryData;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TelemetryRepository
        extends JpaRepository<TelemetryData, Long> {

    List<TelemetryData> findTop100ByDroneIdOrderByTimestampDesc(String droneId);

    Optional<TelemetryData> findFirstByDroneIdOrderByTimestampDesc(String droneId);

    /**
     * Historical samples within a time window, ascending — for mission playback
     * (Epic 4.6).
     */
    Page<TelemetryData> findByDroneIdAndTimestampBetweenOrderByTimestampAsc(
            String droneId, Instant from, Instant to, Pageable pageable);

    long countByDroneId(String droneId);
}
