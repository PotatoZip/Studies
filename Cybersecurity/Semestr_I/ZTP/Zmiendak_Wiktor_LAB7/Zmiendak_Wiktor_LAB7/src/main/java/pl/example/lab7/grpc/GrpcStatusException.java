package pl.example.lab7.grpc;

public class GrpcStatusException extends RuntimeException {
    private final GrpcStatusCode code;

    public GrpcStatusException(GrpcStatusCode code, String message) {
        super(message);
        this.code = code;
    }

    public GrpcStatusCode getCode() {
        return code;
    }
}
