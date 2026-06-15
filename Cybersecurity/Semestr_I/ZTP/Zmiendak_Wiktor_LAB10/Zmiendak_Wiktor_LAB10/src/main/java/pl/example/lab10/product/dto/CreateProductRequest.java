package pl.example.lab10.product.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public class CreateProductRequest {

  @NotBlank
  private String name;

  @Min(0)
  private int stock;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public int getStock() {
    return stock;
  }

  public void setStock(int stock) {
    this.stock = stock;
  }
}
