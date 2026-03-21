package pl.example.lab1.model;

public class ShopOrder {
    private long id;
    private long productId;
    private int quantity;
    private double total;
    private String createdAt;

    public ShopOrder() {}

    public ShopOrder(long id, long productId, int quantity, double total, String createdAt) {
        this.id = id;
        this.productId = productId;
        this.quantity = quantity;
        this.total = total;
        this.createdAt = createdAt;
    }

    public long getId() { return id; }
    public void setId(long id) { this.id = id; }

    public long getProductId() { return productId; }
    public void setProductId(long productId) { this.productId = productId; }

    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }

    public double getTotal() { return total; }
    public void setTotal(double total) { this.total = total; }

    public String getCreatedAt() { return createdAt; }
    public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }
}
