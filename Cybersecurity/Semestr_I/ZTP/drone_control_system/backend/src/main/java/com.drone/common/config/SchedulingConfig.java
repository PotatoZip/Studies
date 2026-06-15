package com.drone.common.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Enables Spring's scheduling and async support, used by the telemetry batch
 * writer ({@code @Scheduled} flush) and the MAVLink mock simulation runner.
 */
@Configuration
@EnableScheduling
@EnableAsync
public class SchedulingConfig {
}
