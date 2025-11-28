"""
Analiza języka polskiego na przykładzie „Lalki” Bolesława Prusa
Zadanie 3.0 i 4.0 – tokenizacja, stemming, lematyzacja (Morfeusz2)
Porównanie dwóch stemmerów i lematyzacji
"""

import re
import requests
from datetime import datetime
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import morfeusz2

nltk.download("punkt", quiet=True)

# ====== Przygotowanie pliku wyjściowego ======
OUT = "lalka_pl_nlp_report.txt"
f = open(OUT, "w", encoding="utf-8")


def write(line=""):
    f.write(line + "\n")


write("Analiza języka polskiego – „Lalka” (B. Prus)")
write(f"Data analizy: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
write("=" * 80)

# ====== Pobranie i wstępne czyszczenie tekstu ======
URL = "https://wolnelektury.pl/media/book/txt/lalka-tom-pierwszy.txt"
resp = requests.get(URL, timeout=30)
text = re.sub(r"\s+", " ", resp.text.strip())
write(f"\nŹródło tekstu: {URL}")

# ====== Wybór 5 przykładowych zdań ======
sentences = sent_tokenize(text, language="polish")
selected = [s for s in sentences if 10 <= len(s.split()) <= 28][10:15]
write("\n" + "=" * 80)
write("WYBRANE 5 ZDAŃ Z „LALKI”")
write("=" * 80)
for i, s in enumerate(selected, 1):
    write(f"\n{i}. {s}")

# ====== Dwa proste „stemmery” dla języka polskiego ======
PL_VOWELS = "aąeęioóuy"
SUF_A = [
    "owego",
    "owej",
    "ego",
    "emu",
    "ami",
    "ach",
    "om",
    "em",
    "ie",
    "ą",
    "ę",
    "y",
    "a",
    "e",
    "u",
    "i",
    "o",
]
SUF_B = [
    "owie",
    "ości",
    "eniu",
    "aniem",
    "aniu",
    "ając",
    "ać",
    "ąc",
    "ł",
    "ła",
    "li",
    "ły",
] + SUF_A


def stem_A(token):
    w = token.lower()
    for s in sorted(SUF_A, key=len, reverse=True):
        if w.endswith(s) and len(w) - len(s) >= 3:
            return w[: -len(s)]
    return w


def stem_B(token):
    w = token.lower()
    for s in sorted(SUF_B, key=len, reverse=True):
        if w.endswith(s) and len(w) - len(s) >= 3:
            w = w[: -len(s)]
            break
    if len(w) > 3 and w.endswith("i") and (w[-2] not in PL_VOWELS):
        w = w[:-1]
    return w


# ====== Lematyzacja (Morfeusz2) ======
morf = morfeusz2.Morfeusz()


def morf_lemma(token):
    analyses = morf.analyse(token)
    return analyses[0][2][1].lower() if analyses else token.lower()


# ====== Porównanie na poziomie zdań ======
write("\n" + "=" * 80)
write("PORÓWNANIE STEMMERÓW I LEMATYZACJI")
write("=" * 80)

diff_total = 0
token_total = 0

for idx, s in enumerate(selected, 1):
    toks = word_tokenize(s, language="polish")
    write(f"\n{'='*80}\nZDANIE {idx}\n{'='*80}")
    write(f"Oryginał: {s}\n")
    write(
        f"{'Token':<20} {'Stem_A':<16} {'Stem_B':<16} {'Lemma (Morfeusz2)':<25} {'A==B?'}"
    )
    write("-" * 95)

    diffs = 0
    for t in toks:
        if not t.isalpha():
            continue
        a, b, l = stem_A(t), stem_B(t), morf_lemma(t)
        eq = "+" if a == b else "- RÓŻNICA"
        if a != b:
            diffs += 1
        write(f"{t:<20} {a:<16} {b:<16} {l:<25} {eq}")

    words = [t for t in toks if t.isalpha()]
    token_total += len(words)
    diff_total += diffs
    write(f"\nRóżnice między stemmerami: {diffs}\n")

# ====== Statystyki ogólne ======
write("\n" + "=" * 80)
write("STATYSTYKI – PORÓWNANIE STEMMERÓW")
write("=" * 80)

all_words = []
stemsA, stemsB, lemmas = [], [], []
for s in selected:
    toks = [t for t in word_tokenize(s, language="polish") if t.isalpha()]
    all_words.extend(toks)
    stemsA.extend([stem_A(t) for t in toks])
    stemsB.extend([stem_B(t) for t in toks])
    lemmas.extend([morf_lemma(t) for t in toks])

agree = sum(1 for a, b in zip(stemsA, stemsB) if a == b)
diffs = sum(1 for a, b in zip(stemsA, stemsB) if a != b)
write(f"\nŁącznie słów: {len(all_words)}")
write(f"Stemmer_A i Stemmer_B zgodne: {agree} ({agree/len(all_words)*100:.1f}%)")
write(f"Różne wyniki: {diffs} ({diffs/len(all_words)*100:.1f}%)")

# ====== Analiza redukcji słownictwa ======
write("\n" + "=" * 80)
write("REDUKCJA SŁOWNICTWA")
write("=" * 80)
orig = set(w.lower() for w in all_words)
setA, setB, setL = set(stemsA), set(stemsB), set(lemmas)


def red(before, after):
    return (1 - after / before) * 100 if before else 0


write(f"Unikalne słowa oryginalnie: {len(orig)}")
write(f"Po Stem_A: {len(setA)} (redukcja: {red(len(orig), len(setA)):.1f}%)")
write(f"Po Stem_B: {len(setB)} (redukcja: {red(len(orig), len(setB)):.1f}%)")
write(f"Po Lematyzacji: {len(setL)} (redukcja: {red(len(orig), len(setL)):.1f}%)")

# ====== Uwagi końcowe ======
write("\n" + "=" * 80)
write("WNIOSKI")
write("=" * 80)
write(
    """
• W języku polskim stemming (obcinanie końcówek) daje niestabilne i często błędne formy.
• Dwa zastosowane stemmery pokazują różnice w agresywności – drugi usuwa więcej sufiksów.
• Lematyzacja z Morfeuszem2 daje poprawne formy słownikowe („kobietom” → „kobieta”, „poszedłem” → „pójść”).
• Dlatego w analizie języka polskiego lematyzacja jest znacznie dokładniejsza niż stemming.
"""
)

write("\n" + "=" * 80)
write("ANALIZA ZAKOŃCZONA")
write("=" * 80)
f.close()
print(f"\n✓ Analiza zakończona. Wyniki zapisane do: {OUT}")
