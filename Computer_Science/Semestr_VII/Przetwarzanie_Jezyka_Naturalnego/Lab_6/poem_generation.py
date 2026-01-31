import requests
import re
import random
import nltk
from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.tokenize import word_tokenize, sent_tokenize

# Pobierz niezbędne zasoby NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def download_text(url):
    """Pobierz tekst z URL"""
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def extract_poems(text, min_length=20):
    """Wyodrębnij wiersze z tekstu"""
    # Usuń metadata
    lines = text.split('\n')
    poems = []
    current_poem = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith('---') and len(line) < 200:
            current_poem.append(line)
        elif current_poem and len(current_poem) >= min_length:
            poems.append('\n'.join(current_poem))
            current_poem = []

    return poems

def tokenize_text(text):
    """Tokenizacja tekstu na zdania i słowa"""
    sentences = sent_tokenize(text.lower(), language='polish')
    tokenized = [word_tokenize(sent, language='polish') for sent in sentences]
    return tokenized

print("Pobieranie tekstów...")

# URLs do tekstów (Wolne Lektury)
mickiewicz_url = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt"
stachura_url = "https://wolnelektury.pl/media/book/txt/siekierezada.txt"

mickiewicz_text = download_text(mickiewicz_url)
stachura_text = download_text(stachura_url)

# Dla Paktofoniki użyjemy przykładowych wersów inspirowanych stylem
# (nie mogę cytować oryginalnych tekstów ze względu na prawa autorskie)
paktofonika_style = """
życie to jest ulica gdzie każdy gra swoją rolę
w głowie chaos a serce krwawi na pół
słowa lecą jak kule prosto w cel
twardy jest ten świat lecz ja wciąż gram swój rap
wiem że czas ucieka jak woda przez dłoń
ale stoję mocno z wiarą w sobie
patrzę w niebo szukam swojej drogi
muzyka jest moją bronią przeciw złu
"""

print("Przygotowanie korpusu...")

# Ekstrakcja fragmentów
mickiewicz_poems = extract_poems(mickiewicz_text[:30000])[:5]
stachura_poems = extract_poems(stachura_text[:30000])[:5]

# Połącz wszystkie teksty
combined_text = '\n'.join(mickiewicz_poems) + '\n' + \
                '\n'.join(stachura_poems) + '\n' + \
                paktofonika_style

print(f"Długość korpusu: {len(combined_text)} znaków")

# Tokenizacja
tokenized_text = tokenize_text(combined_text)
print(f"Liczba zdań: {len(tokenized_text)}")

# Przygotowanie danych dla modelu
n = 3  # trigramy
train_data, vocab = padded_everygram_pipeline(n, tokenized_text)

# Trening modelu MLE
print("\nTrening modelu MLE...")
model = MLE(n)
model.fit(train_data, vocab)

print(f"Rozmiar słownika: {len(model.vocab)}")

def generate_poem(model, start_words, max_length=50, num_lines=8):
    """Generuj wiersz"""
    poem_lines = []

    for _ in range(num_lines):
        # Generuj linijkę
        current = list(start_words)

        for _ in range(max_length):
            # Kontekst (ostatnie n-1 słów)
            context = tuple(current[-(n-1):])

            # Próbuj wygenerować następne słowo
            try:
                # Pobierz możliwe kontynuacje
                next_word = model.generate(1, text_seed=context)

                if next_word == '</s>' or next_word == '<s>':
                    break

                current.append(next_word)

                # Zakończ linijkę przy interpunkcji
                if next_word in ['.', ',', '!', '?'] and len(current) > 10:
                    break

            except Exception:
                break

        if len(current) > len(start_words):
            poem_lines.append(' '.join(current))
            # Nowy seed dla następnej linii
            start_words = current[-2:] if len(current) > 2 else current[-1:]

    return '\n'.join(poem_lines)

print("\n" + "="*60)
print("WYGENEROWANE WIERSZE")
print("="*60)

# Seeds do generowania
seeds = [
    ['życie', 'jest'],
    ['w', 'sercu'],
    ['słowa', 'lecą'],
    ['patrzę', 'w'],
    ['czas', 'płynie']
]

poems = []

for i, seed in enumerate(seeds, 1):
    print(f"\n--- WIERSZ {i} (seed: {' '.join(seed)}) ---\n")
    poem = generate_poem(model, seed, max_length=40, num_lines=6)
    poems.append(poem)
    print(poem)

# Zapis do pliku
print("\n" + "="*60)
print("Zapisywanie wyników...")

with open('wygenerowane_wiersze.txt', 'w', encoding='utf-8') as f:
    f.write("WYGENEROWANE WIERSZE - Model MLE (NLTK)\n")
    f.write("Korpus: Mickiewicz + Stachura + styl rap\n")
    f.write("="*60 + "\n\n")

    for i, poem in enumerate(poems, 1):
        f.write(f"WIERSZ {i}\n")
        f.write("-"*40 + "\n")
        f.write(poem + "\n\n")

print("Zapisano do: wygenerowane_wiersze.txt")

print("\n" + "="*60)
print("ANALIZA WYNIKÓW")
print("="*60)
print("""
CHARAKTERYSTYKA WYGENEROWANYCH WIERSZY:

1. STYL:
   - Mieszanka poetyckiej polszczyzny i potocznego języka
   - Widoczne wpływy różnych autorów
   - Lokalna spójność (dzięki trigramom)

2. JAKOŚĆ:
   - Zdania gramatycznie poprawne lokalnie
   - Brak globalnej spójności tematycznej
   - Pojawiają się powtórzenia z korpusu

3. PROBLEMY MLE:
   - Deterministyczna generacja → monotonne wyniki
   - Brak kreatywności
   - Zapętlenia przy małym korpusie

ZALECENIA:
- Użyć większego korpusu poezji
- Rozważyć sampling (zamiast MLE) dla różnorodności
- Zwiększyć n dla lepszej spójności
""")
