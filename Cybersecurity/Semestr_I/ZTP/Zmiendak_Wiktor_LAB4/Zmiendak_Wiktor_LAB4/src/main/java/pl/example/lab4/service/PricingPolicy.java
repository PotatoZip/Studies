package pl.example.lab4.service;

import pl.example.lab4.model.Product;

import java.math.BigDecimal;

public interface PricingPolicy {

    BigDecimal calculateDiscount(Product product, int quantity, String discountCode);

    BigDecimal calculateShipping(BigDecimal subtotalAfterDiscount);

    int calculateLoyaltyPoints(BigDecimal finalTotal);
}
