package pl.example.lab8.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import pl.example.lab8.dto.OrderCreateRequest;
import pl.example.lab8.dto.ProductCreateRequest;
import pl.example.lab8.entity.OrderEntity;
import pl.example.lab8.entity.ProductEntity;
import pl.example.lab8.repository.OrderRepository;
import pl.example.lab8.repository.ProductRepository;

import java.math.BigDecimal;
import java.time.Instant;

@Service
public class ShopServiceImpl implements ShopService {

  private final ProductRepository productRepository;
  private final OrderRepository orderRepository;

  public ShopServiceImpl(ProductRepository productRepository, OrderRepository orderRepository) {
    this.productRepository = productRepository;
    this.orderRepository = orderRepository;
  }

  @Override
  public ProductEntity createProduct(ProductCreateRequest req) {
    ProductEntity p = new ProductEntity(null, req.getName(), req.getPrice(), req.getStock());
    return productRepository.save(p);
  }

  @Override
  public ProductEntity getProduct(long id) {
    return productRepository.findById(id).orElseThrow(() -> notFound("Product not found"));
  }

  @Override
  public Page<ProductEntity> searchProducts(String q, BigDecimal minPrice, BigDecimal maxPrice, Pageable pageable) {
    String namePart = q == null ? "" : q;
    BigDecimal min = minPrice == null ? BigDecimal.valueOf(0) : minPrice;
    BigDecimal max = maxPrice == null ? new BigDecimal("9999999999.99") : maxPrice;
    return productRepository.findByNameContainingIgnoreCaseAndPriceBetween(namePart, min, max, pageable);
  }

  @Override
  @Transactional
  public OrderEntity createOrder(OrderCreateRequest req) {
    ProductEntity product = productRepository.findById(req.getProductId())
        .orElseThrow(() -> notFound("Product not found"));

    int quantity = req.getQuantity();
    if (quantity > product.getStock()) {
      throw badRequest("Insufficient stock");
    }

    product.setStock(product.getStock() - quantity);
    productRepository.save(product);

    BigDecimal total = product.getPrice().multiply(BigDecimal.valueOf(quantity));
    OrderEntity order = new OrderEntity(null, product.getId(), quantity, total, Instant.now());
    return orderRepository.save(order);
  }

  @Override
  public OrderEntity getOrder(long id) {
    return orderRepository.findById(id).orElseThrow(() -> notFound("Order not found"));
  }

  @Override
  public Page<OrderEntity> listOrders(Pageable pageable) {
    return orderRepository.findAll(pageable);
  }

  private static ResponseStatusException notFound(String msg) {
    return new ResponseStatusException(HttpStatus.NOT_FOUND, msg);
  }

  private static ResponseStatusException badRequest(String msg) {
    return new ResponseStatusException(HttpStatus.BAD_REQUEST, msg);
  }
}
