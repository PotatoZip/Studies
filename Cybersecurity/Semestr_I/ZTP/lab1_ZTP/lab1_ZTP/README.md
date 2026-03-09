# Lab 1 — Monolit (Spring Boot)

Projekt startowy do laboratoriów (lista 1).

## Wymagania
- Java 17+
- Maven 3.9+

## Uruchomienie
```bash
mvn spring-boot:run
```

Aplikacja: `http://localhost:8080`

## Testy weryfikacyjne
### Ocena 3.0
```bash
mvn -Dtest=Grade3VerificationTest test
```

### Ocena 4.0
```bash
mvn -Dtest=Grade4VerificationTest test
```

## Uwaga
Kod startowy jest celowo niekompletny — testy początkowo nie przechodzą.
