package pl.example.lab9.common;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import pl.example.lab9.productservice.InsufficientStockException;
import pl.example.lab9.productservice.ProductNotFoundException;
import pl.example.lab9.orderservice.OrderNotFoundException;

import java.util.Map;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler({ProductNotFoundException.class, OrderNotFoundException.class})
  @ResponseStatus(HttpStatus.NOT_FOUND)
  public Map<String, String> notFound(RuntimeException ex) {
    return Map.of("error", ex.getMessage());
  }

  @ExceptionHandler(InsufficientStockException.class)
  @ResponseStatus(HttpStatus.CONFLICT)
  public Map<String, String> conflict(RuntimeException ex) {
    return Map.of("error", ex.getMessage());
  }

  @ExceptionHandler(IllegalArgumentException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  public Map<String, String> badRequest(RuntimeException ex) {
    return Map.of("error", ex.getMessage());
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  public Map<String, String> validation(MethodArgumentNotValidException ex) {
    String message = ex.getBindingResult().getFieldErrors().stream()
        .findFirst()
        .map(error -> error.getField() + ": " + error.getDefaultMessage())
        .orElse("Validation error");
    return Map.of("error", message);
  }
}
