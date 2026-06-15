# LAB 5 - Cryptographic Libraries Demo

## Struktura

- [cryptography_demo.py](cryptography_demo.py) - osobny program dla biblioteki `cryptography`
- [pycryptodome_demo.py](pycryptodome_demo.py) - osobny program dla biblioteki `pycryptodome`
- [sample_input.txt](sample_input.txt) - plik wejściowy do demonstracji
- [outputs/](outputs) - katalog z wynikami generowanymi przez oba skrypty

## Uruchomienie

```powershell
python cryptography_demo.py sample_input.txt
python pycryptodome_demo.py sample_input.txt
```

Każdy program czyta dane z pliku, wykonuje szyfrowanie i odszyfrowywanie, liczy hashe, tworzy podpis cyfrowy i zapisuje wyniki do swojego podkatalogu w `outputs/`.

## Pokrycie polecenia

- Dwie biblioteki kryptograficzne: tak.
- Osobny program dla każdej biblioteki: tak.
- Dane z pliku: tak.
- Dwa algorytmy symetryczne: AES-CBC i AES-GCM.
- Dwa algorytmy asymetryczne: RSA-OAEP i RSA-PKCS1v15.
- Dwie funkcje skrótu: SHA-256 i SHA-512.
- Podpis cyfrowy: RSA-PSS.

## Ważna uwaga o FIPS

- `cryptography` może korzystać z OpenSSL, więc jest to jedyna część projektu, którą można sensownie powiązać z backendem FIPS-capable.
- `pycryptodome` jest tutaj użyte jako praktyczna biblioteka porównawcza, ale nie jest publicznie przedstawiane jako CMVP/FIPS 140 validated.
- Jeśli prowadzący wymaga ścisłego CMVP dla obu bibliotek, trzeba będzie podmienić drugą bibliotekę na pakiet z rzeczywistym, potwierdzonym modułem FIPS.

## Porównanie

| Kryterium      | cryptography                             | pycryptodome                   |
| -------------- | ---------------------------------------- | ------------------------------ |
| Łatwość użycia | wysoka                                   | wysoka                         |
| Dokumentacja   | bardzo dobra                             | dobra                          |
| Szybkość       | zwykle bardzo dobra, bo oparta o OpenSSL | dobra                          |
| FIPS / CMVP    | zależne od backendu OpenSSL              | brak publicznej walidacji CMVP |

## Uwagi techniczne

- Pliki wynikowe są zapisywane w `outputs/cryptography/` oraz `outputs/pycryptodome/`.
- Implementacja używa RSA w trybie blokowym, żeby spełnić wymóg demonstracji szyfrowania danych z pliku przy użyciu klucza publicznego i prywatnego.
