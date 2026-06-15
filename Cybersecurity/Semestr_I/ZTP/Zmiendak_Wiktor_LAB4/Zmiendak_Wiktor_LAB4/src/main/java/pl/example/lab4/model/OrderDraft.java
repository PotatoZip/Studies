package pl.example.lab4.model;

public class OrderDraft {

    private final Long productId;
    private final int quantity;
    private final String discountCode;

    public OrderDraft(Long productId, int quantity, String discountCode) {
        this.productId = productId;
        this.quantity = quantity;
        this.discountCode = discountCode;
    }

    public Long getProductId() {
        return productId;
    }

    public int getQuantity() {
        return quantity;
    }

    public String getDiscountCode() {
        return discountCode;
    }
}
