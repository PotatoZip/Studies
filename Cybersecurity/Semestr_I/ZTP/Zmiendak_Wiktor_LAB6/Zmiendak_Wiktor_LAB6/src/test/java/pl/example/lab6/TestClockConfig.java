package pl.example.lab6;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;

@TestConfiguration
public class TestClockConfig {

    @Bean
    @Primary
    Clock fixedClock() {
        return Clock.fixed(Instant.parse("2026-04-20T10:15:30Z"), ZoneOffset.UTC);
    }
}
