package pl.example.lab9.contracts;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public class ReserveProductCommand {

  @NotNull
  @Positive
  private Integer quantity;

  public ReserveProductCommand() {
  }

  public ReserveProductCommand(Integer quantity) {
    this.quantity = quantity;
  }

  public Integer getQuantity() {
    return quantity;
  }

  public void setQuantity(Integer quantity) {
    this.quantity = quantity;
  }
}
