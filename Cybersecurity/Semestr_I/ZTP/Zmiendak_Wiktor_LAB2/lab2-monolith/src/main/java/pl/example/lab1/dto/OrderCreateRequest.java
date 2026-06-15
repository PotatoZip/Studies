package pl.example.lab1.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public class OrderCreateRequest {

    @NotNull(message = "Field 'productId' is required")
    private Long productId;

    @NotNull(message = "Field 'quantity' is required")
    @Positive(message = "Field 'quantity' must be an integer > 0")
    private Integer quantity;

    public OrderCreateRequest() {}

    public Long getProductId() { return productId; }
    public void setProductId(Long productId) { this.productId = productId; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }
}
