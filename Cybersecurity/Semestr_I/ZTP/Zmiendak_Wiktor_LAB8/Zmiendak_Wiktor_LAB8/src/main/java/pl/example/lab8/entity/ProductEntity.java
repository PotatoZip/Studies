package pl.example.lab8.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "products")
public class ProductEntity {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  @Column(nullable = false)
  private String name;

  @Column(nullable = false, precision = 19, scale = 2)
  private BigDecimal price;

  @Column(nullable = false)
  private int stock;

  public ProductEntity() {}

  public ProductEntity(Long id, String name, BigDecimal price, int stock) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.stock = stock;
  }

  public Long getId() { return id; }
  public void setId(Long id) { this.id = id; }

  public String getName() { return name; }
  public void setName(String name) { this.name = name; }

  public BigDecimal getPrice() { return price; }
  public void setPrice(BigDecimal price) { this.price = price; }

  public int getStock() { return stock; }
  public void setStock(int stock) { this.stock = stock; }
}
