package pl.example.lab9.productservice;

import java.math.BigDecimal;

public class Product {

  private Long id;
  private String name;
  private BigDecimal price;
  private int stock;

  public Product(Long id, String name, BigDecimal price, int stock) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.stock = stock;
  }

  public Long getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public BigDecimal getPrice() {
    return price;
  }

  public int getStock() {
    return stock;
  }

  public void decreaseStock(int quantity) {
    this.stock -= quantity;
  }
}
