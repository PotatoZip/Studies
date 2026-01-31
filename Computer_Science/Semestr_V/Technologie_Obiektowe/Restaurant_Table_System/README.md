# Restaurant Table System

Aplikacja do efektywnego podglądu oraz zarządzania stolikami w restauracji

## Instalacja

Projekt został zrealizowany przy pomocy pythona v 3.12.6 z wykorzystaniem biblioteki graficznej Tkinter. W celu zainstalowania jej należy posłużyć się komendą:

```bash
pip install tkinter
```

## Uruchomienie

W celu wystartowania programu należy uruchomić plik main.py np za pomocą komendy:

```bash
python -m main.py
```

## Opis Funkcjonalności
Po uruchomieniu aplikacji zostaje wyświetlony główny panel przedstawiający stoliki (numer stolika + liczba krzeseł), przycisk wyświetlający listę zamówień oraz informację o ilości dodatkowych krzeseł na magazynie.

Po wciśnięciu wybranego stolika zostaje wyświetlony panel służący do jego zarządzania. Widzimy na nim podstawowe informacje na temat stolika takie jak numer, stan oraz liczbę krzeseł. Dzięki dostarczonym przyciskom jesteśmy w stanie dodawać oraz resetować liczbę krzeseł przy stole jak również ustawiać jego stan z wolny (zielony kolor) na zajęty (czerwony kolor) oraz do posprzątania (żółty kolor). Dodatkowo w dolnej części tego panelu znajduje się miejsce do zapisywania oraz resetowania zamówienia, które zostanie przypisane do danego stolika.

W panelu głównym znajdziemy szary przycisk otwierający listę wszystkich zamówień przypisanych do stalików.

## License

[MIT](https://choosealicense.com/licenses/mit/)