package pl.example.lab10.order;

import java.time.Instant;

public class Order {

  private final long id;
  private final long productId;
  private final int quantity;
  private final Instant createdAt;
  private OrderStatus status;
  private String rejectionReason;

  public Order(long id, long productId, int quantity, Instant createdAt) {
    this.id = id;
    this.productId = productId;
    this.quantity = quantity;
    this.createdAt = createdAt;
    this.status = OrderStatus.PENDING;
  }

  public long getId() {
    return id;
  }

  public long getProductId() {
    return productId;
  }

  public int getQuantity() {
    return quantity;
  }

  public Instant getCreatedAt() {
    return createdAt;
  }

  public OrderStatus getStatus() {
    return status;
  }

  public String getRejectionReason() {
    return rejectionReason;
  }

  public void confirm() {
    this.status = OrderStatus.CONFIRMED;
    this.rejectionReason = null;
  }

  public void reject(String reason) {
    this.status = OrderStatus.REJECTED;
    this.rejectionReason = reason;
  }
}
