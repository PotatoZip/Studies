package pl.example.lab10.product;

public class InsufficientStockException extends RuntimeException {

  public InsufficientStockException(String message) {
    super(message);
  }
}
