# Sprawozdanie z implementacji algorytmu RSA i testu faktoryzacji

## Wstęp

Celem projektu była własna implementacja prostego, edukacyjnego wariantu algorytmu RSA oraz zbadanie, jak rośnie trudność faktoryzacji wraz ze wzrostem rozmiaru liczb. Program został napisany w Pythonie tak, aby można go było uruchamiać z wiersza poleceń w dwóch trybach. Pierwszy tryb realizuje pełny proces RSA dla tekstu wczytanego z pliku, czyli dzieli wiadomość na bloki, zamienia je na liczby, szyfruje, odszyfrowuje i sprawdza poprawność wyniku. Drugi tryb służy do eksperymentalnej faktoryzacji liczb semipierwszych metodą Pollarda Rho, zapisania wyników do pliku CSV, dopasowania prostych modeli czasowych oraz narysowania wykresu.

W projekcie przyjęto założenie, że kod ma być możliwie prosty i czytelny. Z tego powodu poszczególne etapy zostały rozdzielone na osobne funkcje, a wyniki są zapisywane do osobnych plików tekstowych, JSON oraz CSV. Dzięki temu łatwo prześledzić zarówno działanie algorytmu RSA, jak i zachowanie metody faktoryzacji.

## Dokumentacja własnej implementacji

Program zaczyna się od definicji trzech alfabetów. Pierwszy alfabet zawiera 26 wielkich liter, drugi rozszerza go o małe litery, cyfry, spację i kropkę, a trzeci obejmuje pełne ASCII. Wybór alfabetu ma znaczenie, ponieważ każdy znak musi zostać jednoznacznie zamieniony na liczbę, zanim wiadomość zostanie zaszyfrowana. Za tę część odpowiada funkcja `codec`, która tworzy dwa słowniki: jeden zamienia znak na indeks, a drugi indeks na znak. Dzięki temu konwersja działa w obie strony i jest odwracalna.

Następnie wiadomość jest dzielona na bloki o stałej długości przez funkcję `chunks`. W projekcie przyjęto blok o długości 10 znaków, ponieważ taki podział dobrze odpowiada treści zadania i ułatwia pokazanie działania RSA na małych fragmentach tekstu. Jeśli ostatni blok jest krótszy od wymaganej długości, zostaje uzupełniony pierwszym znakiem wybranego alfabetu. To uzupełnienie jest potrzebne tylko po to, aby każdy blok miał tę samą długość przed zamianą na liczbę.

Samą zamianę bloku tekstu na liczbę wykonuje funkcja `block_to_int`. Działa ona jak zapis liczby w systemie pozycyjnym, tylko że podstawą nie jest 10, lecz rozmiar alfabetu. Każdy kolejny znak przesuwa dotychczasową wartość w lewo i dodaje indeks znaku. Odwrotną operację realizuje `int_to_block`, która przez kolejne dzielenie modulo odtwarza znaki z liczby. Dzięki temu blok tekstowy po konwersji do liczby i ponownie z liczby z powrotem na tekst wraca do swojej pierwotnej postaci.

Zanim wiadomość zostanie zakodowana, program sprawdza jeszcze, czy wszystkie znaki należą do wybranego alfabetu. Służy do tego `check_text_uses_alphabet`. To ważne, bo jeśli użytkownik podałby znak spoza alfabetu, to nie dałoby się go poprawnie zamienić na liczbę. W takim przypadku program zgłasza błąd zamiast wykonywać dalsze obliczenia na niepoprawnych danych.

Kolejnym etapem jest generowanie liczb pierwszych. Funkcja `is_probable_prime` realizuje test Millera-Rabina, który jest testem probabilistycznym. Nie udowadnia on pierwszości w sensie absolutnym, ale przy 40 rundach daje bardzo wysoką pewność praktyczną, wystarczającą dla celów edukacyjnych i kryptograficznych. Funkcja `prime` losuje liczbę o zadanej liczbie bitów, wymusza jej nieparzystość i sprawdza zarówno warunek pierwszości, jak i warunek względnej pierwszości z wykładnikiem `e`.

Najważniejszą częścią jest `rsa_key`, która generuje pełny klucz RSA. Funkcja ta losuje dwie różne liczby pierwsze `p` i `q`, oblicza ich iloczyn `n`, wyznacza funkcję Eulera `phi = (p - 1)(q - 1)`, sprawdza warunek `gcd(e, phi) = 1`, a następnie oblicza odwrotność modularną `d`. W wyniku zwracany jest słownik zawierający `p`, `q`, `n`, `e` i `d`. W naszej implementacji minimalny rozmiar klucza wynosi 768 bitów, ponieważ taki rozmiar został przyjęty w zadaniu i zapewnia odpowiedni poziom trudności w kontekście użytej demonstracji.

Cały proces szyfrowania i odszyfrowywania realizuje funkcja `run_rsa`. Najpierw wczytuje plik wejściowy, sprawdza alfabet, dzieli tekst na bloki, uzupełnia je do pełnej długości i zamienia każdy blok na liczbę całkowitą. Następnie generuje klucz RSA i dla każdego bloku oblicza szyfrogram według wzoru `c = m^e mod n`. Po zaszyfrowaniu program od razu wykonuje odszyfrowanie, licząc `m = c^d mod n`, a później zamienia liczby z powrotem na tekst. Ostatecznie odszyfrowany tekst jest porównywany blok po bloku z tekstem oryginalnym. Dzięki temu można stwierdzić, czy cały łańcuch przekształceń działa poprawnie.

Wyniki działania trybu RSA są zapisywane do kilku plików. Plik `encrypted_blocks.txt` zawiera liczby odpowiadające szyfrogramom, `decrypted_message.txt` zawiera odzyskaną wiadomość, a `block_check.txt` pokazuje porównanie każdego bloku oryginalnego z odszyfrowanym. Dodatkowo plik `rsa_summary.json` zapisuje najważniejsze parametry uruchomienia, takie jak alfabet, długość bloku, liczba bloków, rozmiar klucza, wartość `e`, wartość `n` oraz informację, czy wszystkie bloki zgodziły się po odszyfrowaniu.

Druga część programu dotyczy faktoryzacji. Funkcja `pollard_rho_once` wykonuje jedną próbę rozkładu liczby z użyciem metody Pollarda Rho. Algorytm opiera się na generowaniu pseudolosowego ciągu i szukaniu nietrywialnego dzielnika przez obliczanie największego wspólnego dzielnika różnicy kolejnych wartości z liczbą faktoryzowaną. Funkcja `factor_pollard_rho` powtarza tę próbę wielokrotnie, aby zwiększyć szansę powodzenia. W projekcie liczba prób została ustawiona na 14, a liczba iteracji w pojedynczej próbie jest ograniczona do 2 000 000.

Do samego benchmarku służy `semiprime`, która generuje liczbę będącą iloczynem dwóch liczb pierwszych o zadanej liczbie bitów. Warto zauważyć, że ta funkcja używa małej wartości `e = 3`, ale tylko pomocniczo, przy tworzeniu danych testowych do faktoryzacji. Nie jest to parametr używany do szyfrowania RSA, lecz jedynie ułatwienie techniczne przy generowaniu liczb pierwszych. Funkcja `run_factor` uruchamia cały benchmark dla listy rozmiarów kluczy, mierzy czas działania, zapisuje wyniki do CSV, dopasowuje modele i tworzy wykres. W rezultacie powstają pliki `factorization_results.csv`, `factorization_plot.png` oraz `factorization_analysis.json`.

## Wyniki uzyskane w uruchomieniu RSA

W uruchomionym eksperymencie użyto alfabetu `ascii`, rozmiaru bloku 10 znaków oraz klucza o długości 768 bitów. Wiadomość wejściowa miała 38 znaków i została podzielona na 4 bloki. Wygenerowany klucz miał wykładnik publiczny `e = 65537`, a jego moduł `n` był liczbą 768-bitową. W pliku podsumowującym zapisano również informację `all_blocks_equal = true`, co oznacza, że wszystkie bloki po odszyfrowaniu zgodziły się z blokami oryginalnymi.

Ten wynik pokazuje, że implementacja działa poprawnie. Proces konwersji tekstu na bloki, zamiany bloków na liczby, szyfrowania, odszyfrowania i ponownego złożenia tekstu zachowuje pełną zgodność, o ile spełniony jest warunek `m < n` dla każdego bloku.

## Uzasadnienie wyboru wartości e

W projekcie jako standardową wartość wykładnika publicznego przyjęto `e = 65537`. Jest to jeden z najczęściej stosowanych wyborów w praktyce kryptograficznej, ponieważ łączy w sobie bezpieczeństwo i wydajność. Wartość ta jest liczbą pierwszą i ma bardzo prosty zapis binarny, równy `10000000000000001`. Oznacza to, że potęgowanie modularne wymaga stosunkowo małej liczby mnożeń, więc szyfrowanie jest szybkie. Jednocześnie `65537` jest na tyle duże, że nie wchodzi w typowe problemy znane dla bardzo małych wykładników, takich jak `e = 3`.

Wybór `e = 3` w praktyce mógłby prowadzić do poważnych problemów bezpieczeństwa, zwłaszcza gdy wiadomości nie są odpowiednio zabezpieczone paddingiem. Z kolei `65537` jest od wielu lat uznawane za rozsądny kompromis i stało się de facto standardem. Właśnie dlatego zostało użyte w implementacji RSA jako domyślna wartość wykładnika publicznego.

## Dlaczego RSA wymaga warunku m < n

Warunek `m < n` jest konieczny, ponieważ RSA działa modulo `n`, a więc każda wiadomość jest najpierw redukowana do klasy reszt modulo `n`. Jeśli blok ma wartość większą lub równą `n`, to w praktyce zostaje zastąpiony przez swoją resztę z dzielenia przez `n`. W takim przypadku deszyfrowanie nie odtworzy pierwotnej wiadomości, lecz jedynie wartość `m mod n`.

W trakcie wcześniejszego eksperymentu z małym przykładem `n = 3233` i kluczami `p = 61`, `q = 53` pokazano to bardzo wyraźnie. Dla `m = 500` działa to poprawnie, ponieważ `500 < 3233`, a po zaszyfrowaniu i odszyfrowaniu otrzymuje się z powrotem `500`. Natomiast dla `m = 5000` otrzymano po deszyfrowaniu wartość `1767`, czyli właśnie `5000 mod 3233`. Oznacza to, że oryginalna wartość `5000` została utracona i nie da się jej odzyskać samą operacją RSA.

Z tego powodu w poprawnym zastosowaniu RSA blok wejściowy musi być mniejszy od modułu `n`. W praktyce oznacza to, że rozmiar bloku musi być tak dobrany, aby każda możliwa zakodowana liczba na pewno spełniała warunek `m < n`.

## Dlaczego identyczne bloki dają identyczne szyfrogramy

W „czystym” RSA szyfrowanie jest deterministyczne. Oznacza to, że dla tej samej wiadomości `m` i tego samego klucza publicznego zawsze otrzymuje się ten sam szyfrogram `c`. Jeśli dwa bloki tekstu są identyczne, to po zamianie na liczby również są identyczne, a więc po wykonaniu `c = m^e mod n` otrzymujemy dokładnie ten sam wynik.

To zachowanie jest matematycznie poprawne, ale kryptograficznie niewystarczające. Atakujący może zauważyć powtarzające się szyfrogramy i wnioskować o powtarzających się fragmentach tekstu jawnego. Taki problem ułatwia analizę częstości oraz ataki słownikowe. Jeżeli ktoś zna lub podejrzewa strukturę wiadomości, może porównywać przechwycone szyfrogramy z wcześniej przygotowaną tabelą możliwych bloków.

Właśnie dlatego sam RSA bez dodatkowych zabezpieczeń nie jest stosowany do bezpośredniego szyfrowania danych użytkownika.

## Czym jest padding i jak rozwiązuje problem

Padding to dodatkowe dane wprowadzane do wiadomości przed szyfrowaniem. Jego zadaniem jest zmiana wejścia w taki sposób, aby ten sam tekst jawny nie dawał zawsze tego samego szyfrogramu. Najczęściej padding zawiera losowy składnik, dzięki czemu szyfrowanie staje się niedeterministyczne.

Jednym z najważniejszych schematów paddingu dla RSA jest OAEP, czyli Optimal Asymmetric Encryption Padding. OAEP wykorzystuje losowość oraz funkcje skrótu, aby z jednej wiadomości utworzyć reprezentację, która za każdym razem wygląda inaczej. Dzięki temu ten sam tekst jawny szyfruje się do różnych szyfrogramów, a atakujący nie może już porównywać identycznych bloków po samych wynikach szyfrowania.

OAEP rozwiązuje więc dwa istotne problemy. Po pierwsze, eliminuje deterministyczność RSA. Po drugie, zapewnia bezpieczeństwo semantyczne, czyli utrudnia odróżnienie, czy dwa szyfrogramy pochodzą od tych samych, czy od różnych wiadomości. W praktycznych bibliotekach kryptograficznych RSA prawie zawsze powinno być używane razem z OAEP albo innym bezpiecznym schematem paddingu.

## Jak rośnie trudność faktoryzacji wraz z rozmiarem n

Wyniki benchmarku pokazują bardzo wyraźny wzrost trudności faktoryzacji wraz z rozmiarem liczby. Dla 32 bitów metoda Pollarda Rho znalazła czynniki w około 0,00012 sekundy, a dla 40 bitów w około 0,001 sekundy. Dla 56 bitów czas wzrósł już do około 0,0046 sekundy, dla 64 bitów do około 0,018 sekundy, dla 72 bitów do około 0,096 sekundy, dla 80 bitów do około 0,835 sekundy, a dla 88 bitów do około 6,06 sekundy. Wraz ze wzrostem liczby bitów rosną także liczby iteracji, co potwierdza, że zadanie faktoryzacji bardzo szybko staje się trudniejsze.

W praktyce oznacza to, że nawet jeśli małe liczby można rozkładać bardzo szybko, to dla dużych modułów RSA czas ataku zaczyna rosnąć skrajnie niekorzystnie. Właśnie na tym opiera się bezpieczeństwo RSA. Klucz o długości 768 bitów nadal jest znacznie trudniejszy do złamania niż liczby testowane w benchmarku, a standardowe klucze 2048-bitowe są obecnie uznawane za praktycznie bezpieczne wobec takich prostych metod faktoryzacji.

## Dlaczego wybrano właśnie taki typ funkcji dopasowania

W programie dopasowano trzy typy modeli: liniowy, potęgowy i wykładniczy. Na podstawie wyników najwyższy współczynnik `R^2` uzyskał model wykładniczy, równy około `0.6804`. Model liniowy osiągnął około `0.4185`, a model potęgowy około `0.2540`. Oznacza to, że spośród rozważanych funkcji najlepiej do danych pasuje model wykładniczy.

Wybór tego modelu jest uzasadniony także merytorycznie. Sama metoda Pollarda Rho nie musi w sensie ścisłym rosnąć wykładniczo dla wszystkich zakresów, ale przy tak małym zbiorze pomiarów i w praktycznym zakresie bitów obserwuje się bardzo szybki wzrost kosztu obliczeniowego. Model wykładniczy najlepiej oddaje to przyspieszenie wzrostu w porównaniu z prostą funkcją liniową. Model potęgowy jest tutaj zbyt „łagodny”, a liniowy jeszcze słabiej opisuje gwałtowne wydłużanie czasu dla większych rozmiarów liczb.

Na tej podstawie do ekstrapolacji wykorzystano model wykładniczy jako najlepiej dopasowany do danych eksperymentalnych. Uzyskane prognozy wyniosły około 13,13 sekundy dla 96 bitów, około 5496 sekund dla 128 bitów i około `1.688 × 10^14` sekundy dla 256 bitów. Należy jednak podkreślić, że są to tylko przybliżenia modelowe, a nie rzeczywiste pomiary.

## Czy można ufać tym prognozom dla dużych kluczy

Prognozom dla bardzo dużych kluczy, takich jak 1024, 2048 czy 4096 bitów, nie można ufać bez zastrzeżeń. Ekstrapolacja została wykonana na podstawie bardzo małego zakresu danych, obejmującego tylko liczby 32–88 bitów. Oznacza to, że model został dopasowany do krótkiego fragmentu skali i może zachowywać się zupełnie inaczej poza zakresem pomiarów.

Dodatkowo metoda Pollarda Rho nie jest najlepszym narzędziem do atakowania dużych modułów RSA. Dla większych liczb stosuje się zupełnie inne algorytmy, a ich złożoność rośnie w inny sposób. Z tego powodu wynik modelu należy traktować jedynie jako ilustrację trendu, a nie jako dokładną prognozę realnego czasu łamania dużych kluczy.

Mimo tych ograniczeń sam eksperyment dobrze pokazuje ogólną zasadę. Im większy moduł RSA, tym trudniejsza faktoryzacja i tym większe bezpieczeństwo praktyczne. Właśnie dlatego współcześnie standardem są klucze 2048-bitowe lub większe.

## Wnioski końcowe

Wykonana implementacja spełnia założenia zadania, ponieważ umożliwia zaszyfrowanie i odszyfrowanie wiadomości przy użyciu własnego kodu RSA, a także automatycznie sprawdza zgodność bloków po deszyfrowaniu. Otrzymany wynik dla alfabetu ASCII, wiadomości długości 38 znaków, czterech bloków i klucza 768-bitowego potwierdza poprawność całego procesu, ponieważ wszystkie bloki zostały odtworzone bez błędu.

Projekt pokazuje również, że „czyste” RSA bez paddingu jest rozwiązaniem wyłącznie dydaktycznym. Sama matematyka RSA działa poprawnie, ale bez paddingu pojawiają się problemy z deterministycznością i z bezpieczeństwem praktycznym. Z kolei część faktoryzacyjna pokazuje, jak szybko rośnie koszt rozkładu liczb na czynniki pierwsze oraz dlaczego duże moduły RSA pozostają bezpieczne w praktyce.

Ostatecznie można stwierdzić, że najważniejszymi elementami bezpiecznego RSA są poprawny dobór parametrów, odpowiedni rozmiar klucza oraz stosowanie paddingu, takiego jak OAEP, w rzeczywistych systemach kryptograficznych.
