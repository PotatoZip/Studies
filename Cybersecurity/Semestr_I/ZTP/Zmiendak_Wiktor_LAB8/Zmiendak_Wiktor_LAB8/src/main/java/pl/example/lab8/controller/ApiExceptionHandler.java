package pl.example.lab8.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.server.ResponseStatusException;

import java.util.Map;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(ResponseStatusException.class)
  public ResponseEntity<Map<String, String>> handleResponseStatus(ResponseStatusException ex) {
    HttpStatus status = HttpStatus.resolve(ex.getStatusCode().value());
    if (status == null) status = HttpStatus.INTERNAL_SERVER_ERROR;

    String reason = ex.getReason();
    String message = (reason == null || reason.isBlank()) ? status.getReasonPhrase() : reason;

    return ResponseEntity.status(status).body(Map.of("error", message));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<Map<String, String>> handleValidation(MethodArgumentNotValidException ex) {
    String msg = ex.getBindingResult().getAllErrors().isEmpty()
        ? "Validation failed"
        : ex.getBindingResult().getAllErrors().get(0).getDefaultMessage();
    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Map.of("error", msg));
  }
}
