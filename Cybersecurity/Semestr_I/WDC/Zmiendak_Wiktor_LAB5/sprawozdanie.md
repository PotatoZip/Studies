# Sprawozdanie z ćwiczenia: porównanie biblioteki `cryptography` i narzędzia OpenSSL

Cel zadania

Celem ćwiczenia było przygotowanie dwóch odrębnych programów demonstrujących podstawowe operacje kryptograficzne przy użyciu dwóch różnych rozwiązań dostępnych w ekosystemie Pythona: biblioteki `cryptography` oraz systemowego narzędzia OpenSSL wywoływanego z poziomu CLI. Wybór tych dwóch rozwiązań był podyktowany wymaganiem, aby narzędzia mogły być powiązane ze stanem walidacji FIPS 140‑2 lub FIPS 140‑3, co oznacza, że szczególne znaczenie ma możliwość uruchomienia kodu na binariach lub modułach, które posiadają odpowiednie certyfikaty CMVP/NIST.

Implementacja

W ramach zadania przygotowano dwa osobne skrypty, z których każdy operuje na tym samym pliku wejściowym `sample_input.txt` i wykonuje identyczny zestaw operacji kryptograficznych. Programy odczytują zawartość pliku, wykonują szyfrowanie symetryczne i odszyfrowywanie, realizują operacje asymetryczne (szyfrowanie/dekryptowanie małych bloków, tam gdzie to konieczne), obliczają skróty pliku oraz tworzą i weryfikują podpis cyfrowy. Wyniki każdej operacji zapisywane są do odpowiednich katalogów wyjściowych, dzięki czemu można łatwo porównać wyjścia obu implementacji.

W skrypcie opartym o bibliotekę `cryptography` zrealizowano dwa algorytmy symetryczne: AES‑256‑CBC oraz AES‑256‑GCM. W przypadku trybu CBC zastosowano dopełnienie PKCS7, ponieważ AES w trybie blokowym wymaga pełnych bloków wejściowych. Tryb GCM został wykorzystany jako przykład szyfrowania z uwierzytelnieniem, które zapewnia jednocześnie poufność i integralność danych. W części asymetrycznej zastosowano RSA‑OAEP oraz RSA‑PKCS1v15. Z racji ograniczenia rozmiaru danych, które można bezpośrednio zaszyfrować przy pomocy RSA, zaimplementowano logikę dzielenia danych na bloki (chunking), dzięki czemu możliwe jest zaszyfrowanie dłuższych treści przy pomocy RSA w trybie blokowym. Następnie obliczono dwa skróty: SHA‑256 oraz SHA‑512, a na koniec wygenerowano podpis w trybie RSA‑PSS oraz przeprowadzono jego weryfikację przy użyciu klucza publicznego.

W skrypcie wykorzystującym OpenSSL CLI zrealizowano ten sam zakres funkcji, przy czym dla części symetrycznej zamiast AES‑GCM użyto AES‑CTR w jednym miejscu, ponieważ w niektórych buildach OpenSSL polecenie `openssl enc` może nie obsługiwać rozszerzeń AEAD (to zależy od konkretnej wersji i konfiguracji binariów). W części asymetrycznej wykonano operacje RSA‑OAEP oraz RSA‑PKCS1v15, również z podziałem danych na bloki, ponieważ OpenSSL CLI, podobnie jak biblioteka `cryptography`, nie pozwala na jednorazowe zaszyfrowanie bardzo dużych plików bez zastosowania hybrydowego schematu lub dzielenia danych. W części dotyczącej skrótów obliczono SHA‑256 oraz SHA‑512 za pomocą poleceń OpenSSL, a w części podpisu utworzono i zweryfikowano podpis RSA‑PSS. Skrypt OpenSSL generuje również parę kluczy RSA automatycznie, co upraszcza uruchamianie demonstracji bez konieczności ręcznej przygotowywania materiału kluczowego.

Testowanie

Testy przeprowadzono uruchamiając oba skrypty na pliku `sample_input.txt` znajdującym się w katalogu projektu. Każdy etap demonstracji w obu skryptach został sprawdzony przez porównanie odszyfrowanego wyjścia z oryginalnym plikiem wejściowym oraz przez weryfikację podpisu cyfrowego. Testowe uruchomienia w środowisku deweloperskim potwierdziły poprawność wszystkich wymienionych etapów. W wyniku testów powstały pliki wynikowe w katalogach `outputs/cryptography` oraz `outputs/openssl`, które zawierają zaszyfrowane, odszyfrowane oraz podpisane artefakty.

Środowisko testowe

Do przeprowadzenia ćwiczenia wykorzystano maszynę z systemem Windows. Skrypty uruchamiano przy użyciu interpretera Python w wersji 3.12, a w systemie dostępne było narzędzie OpenSSL zainstalowane jako binarium systemowe. Aby umożliwić reprodukcję wyników, należy sprawdzić wersję interpretera Python poleceniem `python --version`, wersję biblioteki `cryptography` poleceniem `pip show cryptography` oraz wersję OpenSSL poleceniem `openssl version -a`. Wyniki tych poleceń pozwolą potwierdzić, z jakimi konkretnie wersjami pracowano, ponieważ zgodność z FIPS zależy od konkretnego buildu i konfiguracji tych komponentów.

Sprawdzenie zgodności z FIPS / CMVP

Zgodność z FIPS 140‑2 lub FIPS 140‑3 to własność konkretnego modułu kryptograficznego lub binariów, a nie cecha dowolnego fragmentu kodu użytkownika. Dla OpenSSL należy zweryfikować, czy używana instalacja posiada provider FIPS oraz czy dostarczone binaria lub moduły są poświadczone przez CMVP/NIST. W przypadku OpenSSL 3.x FIPS jest dostarczany jako oddzielny provider, którego obecność można sprawdzić poleceniem `openssl list -providers` i poszukaniem pozycji o nazwie `fips`. W starszych instalacjach OpenSSL (1.0/1.1) stosowano oddzielne moduły FIPS i specyficzne buildy; w takich przypadkach weryfikacja zgodności wymaga sprawdzenia dokumentacji i informacji o buildzie dostarczonego binarium.

Aby sprawdzić, czy biblioteka `cryptography` korzysta z OpenSSL z obsługą FIPS, można z poziomu Pythona odczytać tekst identyfikacyjny OpenSSL, którego używa `cryptography`, uruchamiając poniższy jednowiersz w konsoli:

```
python -c "from cryptography.hazmat.bindings.openssl.binding import Binding; print(Binding().openssl_version_text())"
```

Wyjście tego polecenia wskaże, z jakim OpenSSL powiązana jest używana instalacja `cryptography`. Jeżeli w wynikach `openssl list -providers` pojawi się provider o nazwie `fips`, to jest to sygnał, że binaria OpenSSL zawierają provider FIPS. Aby formalnie potwierdzić status CMVP/NIST, należy porównać identyfikator modułu i jego wersję z rekordami na stronie NIST CMVP, ponieważ sama obecność providera nie zastępuje oficjalnej weryfikacji certyfikatowej.

Fragmenty kodu

Poniżej przedstawiono krótkie, reprezentatywne fragmenty kodu, które ilustrują najważniejsze operacje użyte w skryptach demonstracyjnych. Fragmenty zostały skrócone w celu czytelności, jednak ich znaczenie i struktura odpowiadają rozwiązaniu zastosowanemu w projekcie.

Przykład generowania klucza RSA oraz podpisu i weryfikacji przy użyciu biblioteki `cryptography`:

```
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

message = b"dane do podpisu"
signature = private_key.sign(
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256(),
)

public_key.verify(
    signature,
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256(),
)
```

Przykład generowania kluczy RSA z użyciem OpenSSL CLI oraz uruchomienia polecenia z poziomu Pythona w sposób, który nie będzie emitował komunikatów bezpośrednio na konsolę:

```
import subprocess

# generacja klucza prywatnego RSA
subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", "rsa_priv.pem", "-pkeyopt", "rsa_keygen_bits:2048"], check=True, capture_output=True, text=True)

# wyodrębnienie klucza publicznego
subprocess.run(["openssl", "rsa", "-pubout", "-in", "rsa_priv.pem", "-out", "rsa_pub.pem"], check=True, capture_output=True, text=True)
```

Przykład funkcji dzielenia danych na bloki (chunking) użytej dla RSA, aby zaszyfrować większe dane przy pomocy RSA‑OAEP w blokach:

```
def chunk_data(data: bytes, block_size: int):
    for i in range(0, len(data), block_size):
        yield data[i:i+block_size]
```

Uwagi i poprawki do treści sprawozdania

W przygotowanym wcześniej tekście występowało stwierdzenie dotyczące użycia AES‑CTR w implementacji OpenSSL zamiast AES‑GCM; jest to wyjątkowo zależne od wybranego buildu OpenSSL i dlatego poprawne sformułowanie powinno podkreślać, że dostępność AES‑GCM przez `openssl enc` nie jest gwarantowana we wszystkich binariach. Ponadto poprawiono sformułowanie dotyczące zgodności FIPS: biblioteka `cryptography` sama w sobie nie jest certyfikowanym modułem FIPS, natomiast jej zgodność w praktyce zależy od backendu OpenSSL, z którym została zbudowana, oraz od konfiguracji uruchomieniowej.

Porównanie bibliotek

Pod względem łatwości użycia biblioteka `cryptography` dostarcza wysokopoziomowe i idiomatyczne API napisane z myślą o programistach Pythona, dzięki czemu implementacja typowych zadań kryptograficznych jest prostsza, mniej podatna na błędy i bardziej czytelna niż ręczne składanie wywołań do narzędzia CLI. W praktyce oznacza to, że implementacja w `cryptography` wymaga mniej kodu zapośredniczającego, a testowanie oraz utrzymanie takiego rozwiązania jest łatwiejsze, zwłaszcza dla osób, które nie muszą zagłębiać się w niskopoziomowe szczegóły algorytmów. OpenSSL uruchamiany jako zewnętrzne narzędzie CLI daje z kolei bardzo dużą kontrolę nad parametrami i pozwala bezpośrednio obserwować, jakie operacje są wykonywane w warstwie binariów, jednak taka ekspozycja niskiego poziomu wymaga ręcznego konstruowania poleceń, zarządzania plikami tymczasowymi i uważnego ustawiania opcji, co zwiększa złożoność implementacji i ryzyko pomyłek.

Jeżeli chodzi o czytelność dokumentacji, dokumentacja projektu OpenSSL jest obszerna i szczegółowa, lecz ma charakter techniczny i może wymagać większego doświadczenia, aby szybko znaleźć praktyczne przykłady wykorzystania; jest to zaletą w sytuacjach, gdy potrzebna jest niska warstwa kontroli nad parametrami kryptograficznymi. Dokumentacja biblioteki `cryptography` jest natomiast skonstruowana w sposób bardziej przyjazny dla programisty Pythona i zawiera liczne przykłady wysokiego poziomu, co przyspiesza wdrożenie i zmniejsza prawdopodobieństwo typowych błędów implementacyjnych. W zależności od celu pracy, programista może preferować jedną lub drugą dokumentację: OpenSSL dla szczegółowych inspekcji i audytów, `cryptography` dla szybkiego i bezpiecznego developmentu aplikacji.

Pod względem wydajności surowe implementacje algorytmów kryptograficznych zwykle opierają się na zoptymalizowanych, niskopoziomowych bibliotekach (często na OpenSSL), więc przepustowość algorytmów symetrycznych i asymetrycznych jest porównywalna przy tych samych ustawieniach i tym samym kodzie maszynowym. Różnice wydajnościowe pojawiają się natomiast na poziomie integracji: `cryptography` działa wewnątrz procesu Pythona i nie wymaga uruchamiania zewnętrznych procesów ani zapisu tymczasowych plików, dlatego przy wielu krótkich operacjach oraz dla danych o małej i średniej wielkości jej narzut jest zwykle mniejszy niż przy użyciu OpenSSL CLI, które wiąże się z kosztem uruchamiania procesów i operacjami wejścia/wyjścia. Dla bardzo dużych transferów danych, przy założeniu że oba rozwiązania korzystają z tych samych silników kryptograficznych, różnice w surowym throughput będą minimalne.

Z punktu widzenia zgodności i wdrożeń regulowanych najistotniejsze jest to, że formalna certyfikacja FIPS/CMVP dotyczy konkretnego modułu kryptograficznego lub binariów, a nie samego kodu aplikacji. OpenSSL może być dystrybuowany z certyfikowanym providerem FIPS, co czyni go naturalnym kandydatem do środowisk wymagających zgodności z FIPS, pod warunkiem że dana dystrybucja i wersja rzeczywiście posiadają odpowiednie poświadczenia i są poprawnie skonfigurowane. Biblioteka `cryptography` natomiast może działać w sposób zgodny z FIPS tylko wtedy, gdy została zbudowana z odpowiednim backendem OpenSSL i gdy środowisko uruchomieniowe wykorzystuje certyfikowany provider; sama biblioteka nie jest automatycznie świadectwem zgodności. W praktyce, aby uzyskać formalne potwierdzenie zgodności, należy odwołać się do dokumentacji dostawcy binariów i porównać identyfikator modułu oraz wersję z wpisami CMVP/NIST, a także udokumentować konfigurację środowiska uruchomieniowego.

Instrukcja uruchomienia i walidacji wyników

Aby powtórzyć testy, z katalogu projektu należy wykonać polecenia `python cryptography_demo.py` oraz `python openssl_demo.py`. Po poprawnym uruchomieniu w katalogu `outputs/cryptography` oraz `outputs/openssl` pojawią się pliki wynikowe: zaszyfrowane i odszyfrowane oraz pliki zawierające podpisy i skróty. Oryginalny plik wejściowy można porównać z odszyfrowanym plikiem wynikowym, co jest podstawowym krokiem weryfikacyjnym potwierdzającym poprawność szyfrowania i odszyfrowania. Dodatkowo warto zapisać fragmenty wyjścia konsoli lub zrzuty ekranu przedstawiające pozytywne komunikaty z uruchomień, aby dołączyć je jako dowód do sprawozdania.

Podsumowanie

W przygotowanym rozwiązaniu zrealizowano wymagane elementy zadania: dwuetapowe szyfrowanie symetryczne, operacje asymetryczne z dzieleniem na bloki, obliczenia skrótów oraz tworzenie i weryfikację podpisów cyfrowych zarówno przy użyciu biblioteki `cryptography` jak i narzędzia OpenSSL. W sprawozdaniu doprecyzowano sposób weryfikacji zgodności FIPS/CMVP oraz dodano fragmenty kodu i instrukcje środowiskowe, które umożliwiają reprodukcję testów i jednoznaczne ustalenie, czy użyte binaria i biblioteki mają wymagane właściwości certyfikacyjne.
