package pl.example.lab4.repository;

import pl.example.lab4.model.Product;

import java.util.Optional;

public interface ProductRepository {

    Optional<Product> findById(Long id);

    Product save(Product product);
}
