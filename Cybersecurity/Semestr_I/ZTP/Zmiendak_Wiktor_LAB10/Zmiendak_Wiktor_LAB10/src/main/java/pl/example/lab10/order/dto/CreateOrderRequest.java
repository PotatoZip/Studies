package pl.example.lab10.order.dto;

import jakarta.validation.constraints.Min;

public class CreateOrderRequest {

  @Min(1)
  private long productId;

  @Min(1)
  private int quantity;

  public long getProductId() {
    return productId;
  }

  public void setProductId(long productId) {
    this.productId = productId;
  }

  public int getQuantity() {
    return quantity;
  }

  public void setQuantity(int quantity) {
    this.quantity = quantity;
  }
}
