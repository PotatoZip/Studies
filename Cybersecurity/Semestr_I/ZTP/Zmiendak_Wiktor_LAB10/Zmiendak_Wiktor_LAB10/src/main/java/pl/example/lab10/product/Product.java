package pl.example.lab10.product;

public class Product {

  private final long id;
  private final String name;
  private int stock;

  public Product(long id, String name, int stock) {
    this.id = id;
    this.name = name;
    this.stock = stock;
  }

  public long getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public int getStock() {
    return stock;
  }

  public void decreaseStock(int quantity) {
    this.stock -= quantity;
  }
}
