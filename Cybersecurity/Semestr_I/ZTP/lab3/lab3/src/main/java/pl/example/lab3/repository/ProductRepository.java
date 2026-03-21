package pl.example.lab3.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pl.example.lab3.entity.ProductEntity;

public interface ProductRepository extends JpaRepository<ProductEntity, Long> {
}
