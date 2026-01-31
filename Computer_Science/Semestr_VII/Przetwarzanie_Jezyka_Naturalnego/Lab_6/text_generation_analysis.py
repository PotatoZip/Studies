import os
import re
import requests
from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.util import everygrams


class NLTKNGramGenerator:
    def __init__(self, n=2):
        self.n = n
        self.model = MLE(n)
        self.vocab = None

    def preprocess(self, text):
        """Tokenizes the text"""
        text = re.sub(r"\s+", " ", text)
        tokens = re.findall(r"\b\w+\b|[.,!?;:]", text.lower())
        return tokens

    def train(self, tokens):
        """Trains the MLE model using NLTK"""
        # Dzielimy tokeny na zdania (dla uproszczenia - jedno zdanie = wszystkie tokeny)
        train_data = [tokens]

        # padded_everygram_pipeline przygotowuje dane dla modelu językowego
        train_ngrams, self.vocab = padded_everygram_pipeline(self.n, train_data)

        # Trenujemy model MLE
        self.model.fit(train_ngrams, self.vocab)

    def generate(self, seed, num_words=100, random_seed=None):
        """Generates exactly num_words new words using NLTK MLE model"""
        if isinstance(seed, str):
            seed = seed.lower().split()

        # Używamy ostatnich n-1 słów jako kontekstu
        context = seed[-(self.n - 1) :] if len(seed) >= self.n - 1 else seed

        result = list(seed)
        words_generated = 0

        while words_generated < num_words:
            # Generujemy następne słowo na podstawie kontekstu
            # MLE wybiera najczęstsze słowo dla danego kontekstu
            try:
                # Pobieramy rozkład prawdopodobieństwa dla kontekstu
                context_tuple = tuple(context)

                # Szukamy najczęstszego słowa
                next_word = None
                max_prob = 0

                for word in self.vocab:
                    # Pomijamy tokeny paddingu
                    if word in ["<s>", "</s>"]:
                        continue

                    prob = self.model.score(word, context_tuple)
                    if prob > max_prob:
                        max_prob = prob
                        next_word = word

                if next_word is None or max_prob == 0:
                    break

                result.append(next_word)
                words_generated += 1

                # Aktualizujemy kontekst
                context = result[-(self.n - 1) :]

            except Exception:
                break

        return " ".join(result)


def download_text(url):
    """Downloads text from URL"""
    response = requests.get(url)
    response.encoding = "utf-8"
    return response.text


def extract_book_content(text, start_marker, end_marker):
    """Extracts the main content of the book"""
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start != -1 and end != -1:
        return text[start:end]
    return text


def save_results(filename, content):
    """Saves results to file"""
    os.makedirs("results", exist_ok=True)
    with open(f"results/{filename}", "w", encoding="utf-8") as f:
        f.write(content)


# URLs
sherlock_url = "https://www.gutenberg.org/cache/epub/1661/pg1661.txt"
lalka_url = "https://wolnelektury.pl/media/book/txt/lalka-tom-pierwszy.txt"

print("Pobieranie tekstów...")
sherlock_raw = download_text(sherlock_url)
lalka_raw = download_text(lalka_url)

# Ekstrakcja treści
sherlock_text = extract_book_content(
    sherlock_raw, "A SCANDAL IN BOHEMIA", "End of the Project"
)
lalka_text = extract_book_content(lalka_raw, "---- I ----", "-----")

print(f"Długość Sherlock Holmes: {len(sherlock_text)} znaków")
print(f"Długość Lalki: {len(lalka_text)} znaków\n")

# Analiza dla różnych rozmiarów korpusu
corpus_sizes = [0.1, 0.5, 0.8, 1.0]
n_values = [1, 2, 3]

print("=" * 60)
print("ANALIZA DLA SHERLOCK HOLMES (NLTK MLE)")
print("=" * 60)

for corpus_pct in corpus_sizes:
    print(f"\n--- Korpus: {int(corpus_pct * 100)}% ---")

    corpus_size = int(len(sherlock_text) * corpus_pct)
    corpus = sherlock_text[:corpus_size]

    for n in n_values:
        gen = NLTKNGramGenerator(n=100)
        tokens = gen.preprocess(corpus)
        gen.train(tokens)

        # Seed: ostatnie n słów z korpusu
        seed = tokens[-(n + 1) : -1] if len(tokens) > n else tokens[-n:]
        generated = gen.generate(seed)

        filename = f"sherlock_nltk_n{n}_corpus{int(corpus_pct * 100)}.txt"
        save_results(filename, generated)

        print(f"n={n}: {generated[:150]}...")

print("\n" + "=" * 60)
print("ANALIZA DLA LALKI (NLTK MLE)")
print("=" * 60)

for corpus_pct in corpus_sizes:
    print(f"\n--- Korpus: {int(corpus_pct * 100)}% ---")

    corpus_size = int(len(lalka_text) * corpus_pct)
    corpus = lalka_text[:corpus_size]

    for n in n_values:
        gen = NLTKNGramGenerator(n=n)
        tokens = gen.preprocess(corpus)
        gen.train(tokens)

        seed = tokens[-(n + 1) : -1] if len(tokens) > n else tokens[-n:]
        generated = gen.generate(seed)

        filename = f"lalka_nltk_n{n}_corpus{int(corpus_pct * 100)}.txt"
        save_results(filename, generated)

        print(f"n={n}: {generated[:150]}...")

print("\n" + "=" * 60)
print("PODSUMOWANIE WYNIKÓW")
print("=" * 60)
print(
    """
OCENA WYNIKÓW Z NLTK MLE:

1. N=1 (unigramy):
   - Brak kontekstu → chaotyczny, bezsensowny tekst
   - Powtarzanie najczęstszych słów

2. N=2 (bigramy):
   - Lokalnie poprawne pary słów
   - Brak globalnej spójności
   - Lepiej niż unigramy4

3. N=3 (trigramy):
   - Najlepsza jakość
   - Dłuższe spójne fragmenty
   - Często powtarza fragmenty z korpusu

WPŁYW ROZMIARU KORPUSU:
- 10%: Słaba różnorodność, szybkie zapętlenia
- 50%: Znacząca poprawa, więcej kontekstów
- 80-100%: Optymalna jakość, pełny zasób kontekstów

WNIOSKI:
- MLE prowadzi do deterministycznego powtarzania
- Większy korpus → lepsza generalizacja
- Wyższe n → lepsza jakość, ale większe ryzyko przeuczenia
- NLTK MLE zapewnia profesjonalną implementację z obsługą vocabularium
"""
)

print("\nWszystkie wyniki zapisane w folderze 'results/'")
