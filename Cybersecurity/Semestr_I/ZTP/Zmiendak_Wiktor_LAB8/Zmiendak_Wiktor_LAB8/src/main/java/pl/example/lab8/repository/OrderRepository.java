package pl.example.lab8.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.example.lab8.entity.OrderEntity;

public interface OrderRepository extends JpaRepository<OrderEntity, Long> {
}
