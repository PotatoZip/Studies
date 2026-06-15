package pl.example.lab8.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import pl.example.lab8.entity.ProductEntity;

import java.math.BigDecimal;

public interface ProductRepository extends JpaRepository<ProductEntity, Long> {
  Page<ProductEntity> findByNameContainingIgnoreCaseAndPriceBetween(
      String namePart, BigDecimal minPrice, BigDecimal maxPrice, Pageable pageable
  );
}
