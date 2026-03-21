# Lab 2 (starter) — Warstwowanie monolitu (Java + Spring Boot)

## Cel
Przerób projekt tak, aby:
- kontroler nie zależał bezpośrednio od `InMemoryStore`,
- requesty używały DTO + Bean Validation (`@Valid`),
- logika biznesowa była w warstwie `service`,
- błędy walidacji zwracały JSON w formacie: `{"error":"..."}`.

## Start
```bash
mvn spring-boot:run
```
Aplikacja: http://localhost:8080

## Testy weryfikacyjne (do sprawozdania)
```bash
mvn test
```

> Projekt jest starterem — testy na początku nie przechodzą.
