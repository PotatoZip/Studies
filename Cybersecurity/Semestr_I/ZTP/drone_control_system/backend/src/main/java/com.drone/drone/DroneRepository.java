package com.drone.drone;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface DroneRepository extends JpaRepository<Drone, UUID> {
}