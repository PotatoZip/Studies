package pl.example.lab5.model;

public class Order {
  private long id;
  private long productId;
  private int quantity;
  private double total;

  public Order() {}

  public Order(long id, long productId, int quantity, double total) {
    this.id = id;
    this.productId = productId;
    this.quantity = quantity;
    this.total = total;
  }

  public long getId() { return id; }
  public void setId(long id) { this.id = id; }

  public long getProductId() { return productId; }
  public void setProductId(long productId) { this.productId = productId; }

  public int getQuantity() { return quantity; }
  public void setQuantity(int quantity) { this.quantity = quantity; }

  public double getTotal() { return total; }
  public void setTotal(double total) { this.total = total; }
}
