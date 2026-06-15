package pl.example.lab10.common;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import pl.example.lab10.order.OrderNotFoundException;
import pl.example.lab10.product.InsufficientStockException;
import pl.example.lab10.product.ProductNotFoundException;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(ProductNotFoundException.class)
  public ResponseEntity<ApiError> handleProductNotFound(ProductNotFoundException ex) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiError(ex.getMessage()));
  }

  @ExceptionHandler(OrderNotFoundException.class)
  public ResponseEntity<ApiError> handleOrderNotFound(OrderNotFoundException ex) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiError(ex.getMessage()));
  }

  @ExceptionHandler(InsufficientStockException.class)
  public ResponseEntity<ApiError> handleInsufficientStock(InsufficientStockException ex) {
    return ResponseEntity.status(HttpStatus.CONFLICT).body(new ApiError(ex.getMessage()));
  }

  @ExceptionHandler(IllegalArgumentException.class)
  public ResponseEntity<ApiError> handleIllegalArgument(IllegalArgumentException ex) {
    return ResponseEntity.badRequest().body(new ApiError(ex.getMessage()));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<ApiError> handleValidation(MethodArgumentNotValidException ex) {
    String message = ex.getBindingResult().getFieldErrors().stream()
        .findFirst()
        .map(error -> error.getField() + " " + error.getDefaultMessage())
        .orElse("Validation error");

    return ResponseEntity.badRequest().body(new ApiError(message));
  }

  @ExceptionHandler(UnsupportedOperationException.class)
  public ResponseEntity<ApiError> handleTodo(UnsupportedOperationException ex) {
    return ResponseEntity.status(HttpStatus.NOT_IMPLEMENTED).body(new ApiError(ex.getMessage()));
  }
}
