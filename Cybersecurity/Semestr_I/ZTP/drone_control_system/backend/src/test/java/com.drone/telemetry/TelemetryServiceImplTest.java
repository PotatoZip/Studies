package com.drone.telemetry;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.drone.telemetry.dto.TelemetryRequest;
import com.drone.telemetry.dto.TelemetryResponse;
import com.drone.telemetry.model.TelemetryData;
import com.drone.telemetry.repository.TelemetryRepository;
import com.drone.telemetry.service.impl.TelemetryServiceImpl;
import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

@ExtendWith(MockitoExtension.class)
class TelemetryServiceImplTest {

    @Mock private TelemetryRepository repository;
    @InjectMocks private TelemetryServiceImpl service;

    private TelemetryData entity(String droneId) {
        return TelemetryData.builder()
                .droneId(droneId)
                .timestamp(Instant.parse("2026-06-01T00:00:00Z"))
                .latitude(51.5)
                .longitude(-0.12)
                .altitudeMeters(100.0)
                .speedMetersPerSecond(5.0)
                .batteryPercentage(80.0)
                .build();
    }

    @Test
    void processIncomingPersistsMappedEntity() {
        TelemetryRequest request = new TelemetryRequest();
        request.setDroneId("drone-1");
        request.setLatitude(51.5);
        request.setLongitude(-0.12);
        request.setAltitude(100.0);
        request.setSpeed(5.0);
        request.setBattery(80.0);

        service.processIncomingTelemetry(request);

        ArgumentCaptor<TelemetryData> captor = ArgumentCaptor.forClass(TelemetryData.class);
        verify(repository).save(captor.capture());
        TelemetryData saved = captor.getValue();
        assertThat(saved.getDroneId()).isEqualTo("drone-1");
        assertThat(saved.getAltitudeMeters()).isEqualTo(100.0);
        assertThat(saved.getTimestamp()).isNotNull();
    }

    @Test
    void getRecentMapsEntitiesToResponses() {
        when(repository.findTop100ByDroneIdOrderByTimestampDesc("drone-1"))
                .thenReturn(List.of(entity("drone-1")));

        List<TelemetryResponse> result = service.getRecentTelemetry("drone-1");

        assertThat(result).hasSize(1);
        assertThat(result.get(0).getDroneId()).isEqualTo("drone-1");
        assertThat(result.get(0).getBattery()).isEqualTo(80.0);
    }

    @Test
    void getHistoryMapsPagedResults() {
        Instant from = Instant.parse("2026-05-31T00:00:00Z");
        Instant to = Instant.parse("2026-06-01T00:00:00Z");
        Pageable pageable = PageRequest.of(0, 10);
        Page<TelemetryData> page = new PageImpl<>(List.of(entity("drone-1")), pageable, 1);
        when(repository.findByDroneIdAndTimestampBetweenOrderByTimestampAsc(
                eq("drone-1"), any(), any(), any())).thenReturn(page);

        Page<TelemetryResponse> result = service.getHistory("drone-1", from, to, pageable);

        assertThat(result.getTotalElements()).isEqualTo(1);
        assertThat(result.getContent().get(0).getDroneId()).isEqualTo("drone-1");
    }
}
