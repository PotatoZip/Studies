package pl.example.lab8.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "orders")
public class OrderEntity {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private Long productId;

  @Column(nullable = false)
  private int quantity;

  @Column(nullable = false, precision = 19, scale = 2)
  private BigDecimal total;

  @Column(nullable = false)
  private Instant createdAt;

  public OrderEntity() {}

  public OrderEntity(Long id, Long productId, int quantity, BigDecimal total, Instant createdAt) {
    this.id = id;
    this.productId = productId;
    this.quantity = quantity;
    this.total = total;
    this.createdAt = createdAt;
  }

  public Long getId() { return id; }
  public void setId(Long id) { this.id = id; }

  public Long getProductId() { return productId; }
  public void setProductId(Long productId) { this.productId = productId; }

  public int getQuantity() { return quantity; }
  public void setQuantity(int quantity) { this.quantity = quantity; }

  public BigDecimal getTotal() { return total; }
  public void setTotal(BigDecimal total) { this.total = total; }

  public Instant getCreatedAt() { return createdAt; }
  public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
