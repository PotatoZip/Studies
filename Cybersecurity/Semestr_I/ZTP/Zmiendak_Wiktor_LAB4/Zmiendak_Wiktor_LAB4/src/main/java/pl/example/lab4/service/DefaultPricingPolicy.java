package pl.example.lab4.service;

import pl.example.lab4.model.Product;

import java.math.BigDecimal;
import java.math.RoundingMode;

public class DefaultPricingPolicy implements PricingPolicy {

    private static final BigDecimal ZERO = money("0.00");
    private static final BigDecimal DELIVERY_COST = money("15.00");
    private static final BigDecimal FREE_SHIPPING_THRESHOLD = money("300.00");
    private static final BigDecimal SAVE10 = money("0.10");
    private static final BigDecimal BULK5 = money("0.05");
    private static final BigDecimal VIP = money("0.15");

    @Override
    public BigDecimal calculateDiscount(Product product, int quantity, String discountCode) {
        String code = normalizeCode(discountCode);
        BigDecimal sub = subtotal(product, quantity);

        switch (code) {
            case "SAVE10":
                return percent(sub, SAVE10);
            case "BULK5":
                if (quantity >= 5) {
                    return percent(sub, BULK5);
                }
                return ZERO;
            case "VIP":
                return percent(sub, VIP);
            default:
                return ZERO;
        }
    }

    @Override
    public BigDecimal calculateShipping(BigDecimal subtotalAfterDiscount) {
        if (subtotalAfterDiscount.compareTo(FREE_SHIPPING_THRESHOLD) >= 0) {
            return ZERO;
        }
        return DELIVERY_COST;
    }

    @Override
    public int calculateLoyaltyPoints(BigDecimal finalTotal) {
        return finalTotal.divide(BigDecimal.TEN, 0, RoundingMode.DOWN).intValue();
    }

    private BigDecimal subtotal(Product product, int quantity) {
        return product.getPrice()
                .multiply(BigDecimal.valueOf(quantity))
                .setScale(2, RoundingMode.HALF_UP);
    }

    private BigDecimal percent(BigDecimal value, BigDecimal percent) {
        return value.multiply(percent).setScale(2, RoundingMode.HALF_UP);
    }

    private String normalizeCode(String discountCode) {
        if (discountCode == null) {
            return "";
        }
        return discountCode.trim().toUpperCase();
    }

    private static BigDecimal money(String value) {
        return new BigDecimal(value).setScale(2, RoundingMode.HALF_UP);
    }
}
