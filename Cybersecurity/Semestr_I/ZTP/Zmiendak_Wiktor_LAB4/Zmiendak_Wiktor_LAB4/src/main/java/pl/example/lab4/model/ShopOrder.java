package pl.example.lab4.model;

import java.math.BigDecimal;
import java.time.Instant;

public class ShopOrder {

    private final Long id;
    private final Long productId;
    private final int quantity;
    private final BigDecimal subtotal;
    private final BigDecimal discountAmount;
    private final BigDecimal shippingCost;
    private final BigDecimal total;
    private final int loyaltyPoints;
    private final Instant createdAt;

    public ShopOrder(Long id,
                     Long productId,
                     int quantity,
                     BigDecimal subtotal,
                     BigDecimal discountAmount,
                     BigDecimal shippingCost,
                     BigDecimal total,
                     int loyaltyPoints,
                     Instant createdAt) {
        this.id = id;
        this.productId = productId;
        this.quantity = quantity;
        this.subtotal = subtotal;
        this.discountAmount = discountAmount;
        this.shippingCost = shippingCost;
        this.total = total;
        this.loyaltyPoints = loyaltyPoints;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public Long getProductId() {
        return productId;
    }

    public int getQuantity() {
        return quantity;
    }

    public BigDecimal getSubtotal() {
        return subtotal;
    }

    public BigDecimal getDiscountAmount() {
        return discountAmount;
    }

    public BigDecimal getShippingCost() {
        return shippingCost;
    }

    public BigDecimal getTotal() {
        return total;
    }

    public int getLoyaltyPoints() {
        return loyaltyPoints;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}
