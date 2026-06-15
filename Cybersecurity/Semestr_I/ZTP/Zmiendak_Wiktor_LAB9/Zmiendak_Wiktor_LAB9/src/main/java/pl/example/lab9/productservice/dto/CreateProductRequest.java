package pl.example.lab9.productservice.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;

public class CreateProductRequest {

  @NotBlank
  private String name;

  @NotNull
  @DecimalMin("0.01")
  private BigDecimal price;

  @NotNull
  @Min(0)
  private Integer stock;

  public CreateProductRequest() {
  }

  public CreateProductRequest(String name, BigDecimal price, Integer stock) {
    this.name = name;
    this.price = price;
    this.stock = stock;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public BigDecimal getPrice() {
    return price;
  }

  public void setPrice(BigDecimal price) {
    this.price = price;
  }

  public Integer getStock() {
    return stock;
  }

  public void setStock(Integer stock) {
    this.stock = stock;
  }
}
