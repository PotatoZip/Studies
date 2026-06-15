package pl.example.lab7.config;

public record AppConfig(Mode mode, boolean retryEnabled, boolean cacheEnabled, int maxAttempts) {
    public enum Mode { REST, GRPC }
}
