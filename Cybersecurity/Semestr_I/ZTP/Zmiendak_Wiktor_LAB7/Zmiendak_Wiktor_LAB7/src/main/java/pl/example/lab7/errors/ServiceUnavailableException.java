package pl.example.lab7.errors;

/** Błąd chwilowy (np. 503/timeout/UNAVAILABLE). */
public class ServiceUnavailableException extends RuntimeException {
    public ServiceUnavailableException(String message) { super(message); }
    public ServiceUnavailableException(String message, Throwable cause) { super(message, cause); }
}
