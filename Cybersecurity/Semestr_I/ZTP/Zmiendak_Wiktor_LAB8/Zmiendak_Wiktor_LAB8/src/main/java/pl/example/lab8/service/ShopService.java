package pl.example.lab8.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import pl.example.lab8.dto.OrderCreateRequest;
import pl.example.lab8.dto.ProductCreateRequest;
import pl.example.lab8.entity.OrderEntity;
import pl.example.lab8.entity.ProductEntity;

import java.math.BigDecimal;

public interface ShopService {
  ProductEntity createProduct(ProductCreateRequest req);
  ProductEntity getProduct(long id);
  Page<ProductEntity> searchProducts(String q, BigDecimal minPrice, BigDecimal maxPrice, Pageable pageable);

  OrderEntity createOrder(OrderCreateRequest req);
  OrderEntity getOrder(long id);
  Page<OrderEntity> listOrders(Pageable pageable);
}
