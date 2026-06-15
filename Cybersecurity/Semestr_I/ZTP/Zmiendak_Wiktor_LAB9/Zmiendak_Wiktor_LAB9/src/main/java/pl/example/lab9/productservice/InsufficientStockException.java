package pl.example.lab9.productservice;

public class InsufficientStockException extends RuntimeException {

  public InsufficientStockException(String message) {
    super(message);
  }
}
