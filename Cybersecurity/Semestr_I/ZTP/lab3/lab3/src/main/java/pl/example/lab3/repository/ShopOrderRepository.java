package pl.example.lab3.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.example.lab3.entity.ShopOrderEntity;

public interface ShopOrderRepository extends JpaRepository<ShopOrderEntity, Long> {
}
