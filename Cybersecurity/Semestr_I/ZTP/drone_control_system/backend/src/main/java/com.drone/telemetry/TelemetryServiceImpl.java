package com.drone.telemetry.service.impl;

import com.drone.telemetry.dto.TelemetryRequest;
import com.drone.telemetry.dto.TelemetryResponse;
import com.drone.telemetry.model.TelemetryData;
import com.drone.telemetry.repository.TelemetryRepository;
import com.drone.telemetry.service.TelemetryService;
import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class TelemetryServiceImpl implements TelemetryService {

    private final TelemetryRepository repository;

    @Override
    public void processIncomingTelemetry(TelemetryRequest request) {
        log.info("Received telemetry for drone: {}", request.getDroneId());

        TelemetryData entity = TelemetryData.builder()
                .droneId(request.getDroneId())
                .timestamp(Instant.now())
                .latitude(request.getLatitude())
                .longitude(request.getLongitude())
                .altitudeMeters(request.getAltitude())
                .speedMetersPerSecond(request.getSpeed())
                .batteryPercentage(request.getBattery())
                .build();

        repository.save(entity);
    }

    @Override
    public List<TelemetryResponse> getRecentTelemetry(String droneId) {
        return repository
                .findTop100ByDroneIdOrderByTimestampDesc(droneId)
                .stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    @Override
    public Page<TelemetryResponse> getHistory(String droneId, Instant from, Instant to,
            Pageable pageable) {
        return repository
                .findByDroneIdAndTimestampBetweenOrderByTimestampAsc(droneId, from, to, pageable)
                .map(this::mapToResponse);
    }

    private TelemetryResponse mapToResponse(TelemetryData data) {
        return TelemetryResponse.builder()
                .droneId(data.getDroneId())
                .recordedAt(data.getTimestamp())
                .latitude(data.getLatitude())
                .longitude(data.getLongitude())
                .altitude(data.getAltitudeMeters())
                .speed(data.getSpeedMetersPerSecond())
                .battery(data.getBatteryPercentage())
                .build();
    }
}
