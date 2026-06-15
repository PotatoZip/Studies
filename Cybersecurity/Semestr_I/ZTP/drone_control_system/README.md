# Drone Control System — Dokumentacja projektu

Poniżej znajduje się kompleksowa dokumentacja projektu, opis architektury, instrukcje uruchomienia oraz lista REST i WebSocket endpointów z przykładami użycia.

## Spis treści

- Cel projektu
- Architektura
- Uruchomienie
- Autoryzacja i uwierzytelnianie
- REST API — endpointy
  - Autoryzacja
  - Drony
  - Stan dronów
  - Komendy
  - Telemetria
  - Misje
  - Symulacja
  - Health
- WebSocket / STOMP
- Przykłady użycia
- Pliki konfiguracyjne

## Cel projektu

Celem projektu było przygotowanie systemu do zarządzania i monitoringu floty dronów. Zakłada on dostarczenie możliwości przyjmowania i routowania komend, zbierania telemetrii, zarządzania misjami i interaktywnego komunikowania się z dronem przy pomocy przejrzystego UI.

## Architektura

Architektura systemu została zaprojektowana jako układ warstwowy, w którym backend odpowiada za logikę domenową, integracje i bezpieczeństwo, a frontend za wygodną prezentację danych oraz sterowanie dronami. Po stronie serwera wykorzystano Java Spring Boot, ponieważ dobrze wspiera tworzenie REST API, mechanizmów bezpieczeństwa oraz walidacji żądań.

Frontend został zbudowany w React z TypeScriptem, dzięki czemu interfejs pozostaje spójny, typowany i łatwy do rozwijania. Taki wybór upraszcza tworzenie ekranów operacyjnych, widoków mapowych, paneli statusu i formularzy do wydawania komend.

Wewnątrz backendu system został podzielony na moduły odpowiadające za konkretne obszary funkcjonalne. Moduł `authentication` obsługuje logowanie, rejestrację i wydawanie tokenów JWT. Moduł `drone` odpowiada za trwałe dane o dronach oraz ich podstawowe operacje administracyjne. Moduł `telemetry` przetwarza pomiary i udostępnia ich historię. Moduł `command` zajmuje się przyjmowaniem, kolejkowaniem i rozsyłaniem komend. Moduł `mission` zarządza misjami i ich przypisaniami do dronów. Moduł `simulation` pozwala uruchamiać kontrolowane scenariusze testowe, a moduł `websocket` odpowiada za publikację zdarzeń w czasie rzeczywistym.

Komunikacja runtime w projekcie została rozdzielona na dwa główne kanały. REST API obsługuje operacje wymagające klasycznego żądania i odpowiedzi, takie jak tworzenie misji, zarządzanie dronami czy pobieranie historii telemetrii. STOMP-over-WebSocket został wykorzystany tam, gdzie ważny jest strumień danych i reakcja w czasie rzeczywistym, czyli przede wszystkim przy telemetrycznych aktualizacjach oraz prywatnych potwierdzeniach komend.

## Uruchomienie

1. Wymagania do lokalnego uruchomienia środowisak:

- Java 17+
- Maven
- Node.js
- Docker

2. Uruchomienie backendu:

```bash
cd backend
mvn clean install
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.config.location=classpath:/application-docker.properties"
```

Domyślnie API nasłuchuje na porcie skonfigurowanym w pliku `application.properties`. W tym repo przykład używa `http://localhost:8081`

3. Uruchomieniu frontendu:

```bash
cd frontend
npm install
npm run dev
```

Domyślny dev server Vite: `http://localhost:5173`

4. Uruchomienie przy pomocy Docker Compose (zalecane):

```bash
docker-compose up --build
```

## Autoryzacja i uwierzytelnianie

Warstwa autoryzacji w tym projekcie opiera się na tokenach JWT i obejmuje zarówno wywołania REST, jak i komunikację WebSocket. Użytkownik zaczyna od rejestracji lub logowania przez publiczne endpointy z prefiksu `/api/v1/auth`, a po poprawnym uwierzytelnieniu otrzymuje token, który musi być dołączany do kolejnych żądań. Token ten jest podstawą identyfikacji operatora po stronie backendu i pozwala systemowi przypisać wykonane operacje do konkretnego konta.

Wszystkie endpointy inne niż rejestracja, logowanie i odczyt własnego profilu wymagają nagłówka HTTP `Authorization: Bearer <JWT>`. Oznacza to, że bez ważnego tokena API odrzuci próby wykonania operacji związanych z dronami, misjami, komendami, telemetrią i symulacją. Taki model zabezpieczeń zapewnia jednolity mechanizm kontroli dostępu dla całej aplikacji i upraszcza integrację po stronie frontendu.

Mechanizm autoryzacji obejmuje również warstwę WebSocket. W czasie inicjacji połączenia STOMP klient przekazuje ten sam token w natywnym nagłówku `Authorization`, a serwer weryfikuje go podczas zdarzenia `CONNECT`. Po poprawnej walidacji nadawca zostaje przypisany do sesji i dzięki temu odpowiedzi typu ACK mogą być dostarczane do właściwego operatora przez prywatną kolejkę użytkownika. To podejście jest ważne, ponieważ komendy dla dronów są wykonywane asynchronicznie.

Przykład pobrania tokena przy pomocy PowerShell:

```powershell
$login = @{ username = 'operator'; password = 'pass' } | ConvertTo-Json
$res = Invoke-RestMethod -Uri "http://localhost:8081/api/v1/auth/login" -Method Post -ContentType "application/json" -Body $login
$TOKEN = $res.token
```

## REST API — lista endpointów

REST API stanowi główny interfejs administracyjny i operacyjny systemu. Wszystkie ścieżki są osadzone pod bazowym prefiksem `http://{host}:{port}`, przy czym w środowisku lokalnym oznacza to adres `http://localhost:8081`. API zostało podzielone na logiczne grupy, dzięki czemu osobne obszary funkcjonalne nie mieszają się ze sobą i można je łatwo odnaleźć zarówno po stronie frontendowej, jak i podczas testów ręcznych.

Sekcja autoryzacji pod `/api/v1/auth` obejmuje trzy podstawowe operacje:

- Endpoint `POST /api/v1/auth/register`: Służy do tworzenia nowego konta operatora i przyjmuje dane opisane przez `RegisterRequest`, czyli informacje potrzebne do utworzenia użytkownika, takie jak nazwa konta, hasło i opcjonalnie dane kontaktowe. Odpowiedź zwraca obiekt `AuthResponse` z tokenem JWT, dzięki czemu nowo zarejestrowany użytkownik może od razu rozpocząć pracę bez dodatkowego logowania.
- Endpoint `POST /api/v1/auth/login`: Realizuje standardowe uwierzytelnienie na podstawie danych z `LoginRequest`. Po poprawnej weryfikacji zwraca również `AuthResponse` z tokenem, który należy wykorzystywać przy kolejnych wywołaniach.
- Endpoint `GET /api/v1/auth/me`: Pozwala frontendowi sprawdzić, kim jest aktualnie zalogowany użytkownik i zwraca podstawowy profil obejmujący nazwę oraz rolę.

W obszarze kontroli stanu aplikacji dostępny jest prosty endpoint `GET /api/v1/health`, którego zadaniem jest potwierdzenie, że backend działa i odpowiada poprawnie. Powinien on zwracać tekst `OK`.

Sekcja dronów obsługuje podstawowy cykl życia rekordu drona:

- `POST /api/v1/drones`: Tworzy nowy wpis w systemie.
- `GET /api/v1/drones`: Zwraca pełną listę dronów.
- `GET /api/v1/drones/{id}`: Umożliwia odczyt konkretnego obiektu po identyfikatorze UUID.
- `DELETE /api/v1/drones/{id}`: Usuwa rekord z systemu.
- `PATCH /api/v1/drones/{id}/status`: Pozwala zaktualizować aktualny status operacyjny drona.

Podobną rolę pełni sekcja stanu dronów, która nie służy do zarządzania samym rekordem, lecz do odczytu aktualnego, cache'owanego obrazu floty:

- `GET /api/v1/drones/state`: Zwraca listę wszystkich aktywnych dronów.
- `GET /api/v1/drones/state/{droneId}`: Pobiera stan konkretnej jednostki.

Sekcja komend obsługuje asynchroniczne sterowanie dronami. Najbardziej uniwersalny wariant stanowi `POST /api/v1/commands`, który przyjmuje `CommandRequest` i pozwala wysłać dowolny typ komendy z jednego miejsca. Dla najczęściej używanych operacji przygotowano wygodne endpointy pomocnicze:

- `POST /api/v1/commands/{droneId}/takeoff`: Inicjuje start i wymaga podania docelowej wysokości.
- `POST /api/v1/commands/{droneId}/land`: Wykonuje lądowanie.
- `POST /api/v1/commands/{droneId}/rtl`: Uruchamia powrót do punktu startowego.
- `POST /api/v1/commands/{droneId}/waypoint`: Wysyła drona do konkretnego punktu zdefiniowanego współrzędnymi geograficznymi i wysokością.
- `GET /api/v1/commands/{droneId}/queue`: Zwraca kolejkę niewyackowanych komend dla wskazanego drona.
- `GET /api/v1/commands/status/{commandId}`: Udostępnia status pojedynczej komendy.

Sekcja telemetrii obsługuje zarówno bezpośrednie przyjęcie danych, jak i ich późniejsze odczytywanie:

- `POST /api/v1/telemetry/ingest`: Służy do ręcznego wstrzyknięcia próbki telemetrycznej i przydaje się podczas testów integracyjnych lub podłączania źródeł spoza natywnego przepływu.
- `GET /api/v1/telemetry/{droneId}/recent`: Zwraca najnowsze próbki dla konkretnego drona.
- `GET /api/v1/telemetry/{droneId}/history`: Udostępnia historię w zadanym przedziale czasu z paginacją.

Sekcja misji odpowiada za zarządzanie scenariuszami operacyjnymi:

- `GET /api/v1/missions`: Zwraca wszystkie misje zapisane w systemie.
- `GET /api/v1/missions/{id}`: Pozwala odczytać szczegóły pojedynczej misji.
- `POST /api/v1/missions`: Tworzy nową misję na podstawie `MissionRequest`, który może zawierać nazwę, listę dronów oraz pozostałe parametry planu.
- `POST /api/v1/missions/{missionId}/drones/{droneId}`: Przypisuje drona do już istniejącej misji.
- `POST /api/v1/missions/{id}/start` oraz `POST /api/v1/missions/{id}/stop`: Uruchamiają i zatrzymują wykonanie.

Sekcja symulacji pełni rolę narzędzia testowego dla całego pipeline'u komunikacyjnego:

- `POST /api/simulation/start` oraz `POST /api/simulation/full-pipeline`: Uruchamiają scenariusz symulacyjny, który może działać na podstawie opcjonalnego `SimulationRequest`. Zwracany obiekt `SimulationRunStatus` opisuje identyfikator uruchomienia oraz jego postęp.
- `GET /api/simulation/{runId}`: Pozwala odczytać status pojedynczego runa.
- `GET /api/simulation`: Zwraca listę wszystkich znanych uruchomień.
- `POST /api/simulation/{runId}/stop`: Umożliwia przerwanie aktywnej symulacji.

Przykład logowania za pomocą `curl`:

```bash
curl -X POST http://localhost:8081/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"operator","password":"pass"}'
```

## WebSocket / STOMP

Warstwa WebSocket w tym projekcie została zbudowana wokół STOMP. Punkt wejścia do połączenia znajduje się pod adresem `/ws`, a obsługa SockJS została włączona po to, aby klient mógł skorzystać z fallbacku w środowiskach, w których natywne WebSockety nie są dostępne lub wymagają dodatkowej kompatybilności.

Broker wiadomości został skonfigurowany z dwoma podstawowymi przestrzeniami destynacji. Przestrzeń `/topic` służy do broadcastu informacji do wszystkich klientów, natomiast przestrzeń `/queue` obsługuje bardziej ukierunkowane kolejki. Z kolei prefiks aplikacyjny `/app` wskazuje, że wiadomości wysyłane do tej przestrzeni są obsługiwane po stronie serwera i mogą inicjować dalsze przetwarzanie. Prefiks użytkownika `/user` pozwala dostarczać wiadomości do konkretnego użytkownika.

W praktyce WebSocket jest wykorzystywany głównie do telemetrii oraz potwierdzeń komend. Kanał `/topic/telemetry` rozsyła wszystkie próbki telemetryczne do widoków globalnych, takich jak dashboard floty, natomiast `/topic/telemetry/{droneId}` pozwala przesyłać dane wyłącznie dla jednego drona. Kanał `/user/queue/acks` dostarcza prywatne informacje o potwierdzeniach komend do użytkownika, który wywołał dane żądanie.

Autoryzacja połączenia WebSocket jest spójna z mechanizmem REST i wykorzystuje ten sam token JWT. Klient przekazuje go w nagłówku `Authorization` podczas fazy `CONNECT`, a serwer waliduje ten token i przypisuje nadawcę do sesji.

## Dalszy rozwój

- Testy z wykorzystaniem prawdziwego drona
- Dodanie OpenAPI/Swagger
- Dodanie przykładowe skrypty uruchomieniowe i testowe
