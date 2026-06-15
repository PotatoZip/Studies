package pl.example.lab7.rest;

public class RestNotFoundException extends RuntimeException {
    public RestNotFoundException(String message) { super(message); }
}
