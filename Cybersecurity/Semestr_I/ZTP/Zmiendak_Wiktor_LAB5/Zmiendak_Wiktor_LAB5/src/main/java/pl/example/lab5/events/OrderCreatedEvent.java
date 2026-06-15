package pl.example.lab5.events;

public class OrderCreatedEvent {
  private String eventId;
  private long orderId;
  private long productId;
  private int quantity;
  private double total;

  public OrderCreatedEvent() {}

  public OrderCreatedEvent(String eventId, long orderId, long productId, int quantity, double total) {
    this.eventId = eventId;
    this.orderId = orderId;
    this.productId = productId;
    this.quantity = quantity;
    this.total = total;
  }

  public String getEventId() { return eventId; }
  public void setEventId(String eventId) { this.eventId = eventId; }

  public long getOrderId() { return orderId; }
  public void setOrderId(long orderId) { this.orderId = orderId; }

  public long getProductId() { return productId; }
  public void setProductId(long productId) { this.productId = productId; }

  public int getQuantity() { return quantity; }
  public void setQuantity(int quantity) { this.quantity = quantity; }

  public double getTotal() { return total; }
  public void setTotal(double total) { this.total = total; }
}
