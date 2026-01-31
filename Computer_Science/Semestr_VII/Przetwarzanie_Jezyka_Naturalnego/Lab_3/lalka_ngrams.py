#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Task 5 (PL) – 'Lalka' (B. Prus): porównanie n-gramów (1..4)
Warianty:
  • normalizacja: none / stem_A / stem_B / lemma (Morfeusz2 – jeśli dostępny)
  • stopwords: keep / remove
Wyjście:
  • katalog: ngrams_lalka/
  • raport:  ngrams_lalka/lalka_pl_ngrams_report.txt (uporządkowany)
  • CSV:     ngrams_lalka/ngrams_n{1..4}__{norm}__{keep|remove}.csv
"""

import csv
import os
from pathlib import Path
import re
import string
from collections import Counter
from datetime import datetime
from typing import List, Tuple

import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# ========== USTAWIENIA ==========
SRC_URL = "https://wolnelektury.pl/media/book/txt/lalka-tom-pierwszy.txt"
OUT_DIR = Path("ngrams_lalka")
OUT_TXT = OUT_DIR / "lalka_pl_ngrams_report.txt"

TOP_K = 20  # ile najczęstszych n-gramów pokazywać w raporcie/CSV
N_MAX = 4  # maksymalna długość n-gramu (1..N_MAX)

# ========== PRZYGOTOWANIE ==========
OUT_DIR.mkdir(parents=True, exist_ok=True)

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Stopwords PL – bezpieczny fallback (NLTK zwykle nie ma "polish")
try:
    POLISH_STOP = set(w.lower() for w in stopwords.words("polish"))
except (OSError, LookupError):
    print("⚠️  Brak oficjalnych stopwords PL w NLTK – używam listy awaryjnej.")
    POLISH_STOP = {
        "i",
        "w",
        "na",
        "że",
        "a",
        "do",
        "z",
        "się",
        "o",
        "jak",
        "nie",
        "to",
        "po",
        "co",
        "tak",
        "dla",
        "ale",
        "od",
        "za",
        "jest",
        "był",
        "była",
        "było",
        "być",
        "jego",
        "jej",
        "ich",
        "go",
        "tego",
        "ten",
        "ta",
        "to",
        "te",
        "tym",
        "tam",
        "czy",
        "która",
        "który",
        "które",
        "którym",
        "którego",
        "którą",
        "gdzie",
        "kiedy",
        "już",
        "jeszcze",
        "nad",
        "pod",
        "przez",
        "także",
        "więc",
        "tu",
        "tam",
        "mnie",
        "tobie",
        "sobie",
        "nas",
        "was",
        "może",
        "bo",
        "albo",
        "gdy",
        "gdyż",
    }

# Lematyzacja (Morfeusz2 – opcjonalnie)
try:
    import morfeusz2

    _morf = morfeusz2.Morfeusz()
except Exception as e:
    _morf = None
    print("ℹ️  Morfeusz2 niedostępny – wariant 'lemma' zostanie pominięty.")
    print(f"   Szczegóły: {e}")


# ========== FUNKCJE POMOCNICZE ==========
def fetch_text(url: str) -> str:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    txt = resp.text
    txt = re.sub(r"\s+", " ", txt.strip())
    return txt


PL_CHARS = "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ"


def is_alpha_pl(token: str) -> bool:
    return all(ch.isalpha() or ch in PL_CHARS for ch in token)


def tokenize_pl_words(text: str) -> List[str]:
    raw = word_tokenize(text, language="polish")
    return [t.lower() for t in raw if is_alpha_pl(t)]


# Dwa „stemmery” edukacyjne (proste ucinanie sufiksów)
PL_VOWELS = "aąeęioóuy"
PL_COMMON_SUFFIXES_A = [
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
PL_COMMON_SUFFIXES_B = [
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
] + PL_COMMON_SUFFIXES_A


def stem_A(w: str) -> str:
    w = w.lower()
    for suf in sorted(PL_COMMON_SUFFIXES_A, key=len, reverse=True):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def stem_B(w: str) -> str:
    w = w.lower()
    for suf in sorted(PL_COMMON_SUFFIXES_B, key=len, reverse=True):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            w = w[: -len(suf)]
            break
    if len(w) > 3 and w.endswith("i") and (w[-2] not in PL_VOWELS):
        w = w[:-1]
    return w


def lemma_morf(w: str) -> str:
    if _morf is None:
        return w.lower()
    analyses = _morf.analyse(w)
    return analyses[0][2][1].lower() if analyses else w.lower()


def normalize(tokens: List[str], mode: str) -> List[str]:
    if mode == "none":
        return tokens
    if mode == "stem_A":
        return [stem_A(t) for t in tokens]
    if mode == "stem_B":
        return [stem_B(t) for t in tokens]
    if mode == "lemma":
        if _morf is None:
            raise RuntimeError("Morfeusz2 not available but 'lemma' requested.")
        return [lemma_morf(t) for t in tokens]
    raise ValueError(f"Unknown normalization mode: {mode}")


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in POLISH_STOP]


def make_ngrams(seq: List[str], n: int) -> List[str]:
    return (
        [" ".join(seq[i : i + n]) for i in range(0, len(seq) - n + 1)] if n > 0 else []
    )


# Formatowanie tabel w raporcie
def fmt_table(rows: List[Tuple[str, int, float]], widths=(6, 52, 10, 9)) -> str:
    out_lines = []
    out_lines.append(
        f"{'rank':<{widths[0]}}{'ngram':<{widths[1]}}{'count':>{widths[2]}}{'share%':>{widths[3]}}"
    )
    out_lines.append("-" * sum(widths))
    for r, (ng, c, share) in enumerate(rows, 1):
        out_lines.append(
            f"{r:<{widths[0]}}{ng[:widths[1]-2]:<{widths[1]}}{c:>{widths[2]}}{share:>{widths[3]}.2f}"
        )
    return "\n".join(out_lines)


# ========== GŁÓWNA LOGIKA ==========
def main():
    print("▶ Pobieram i przygotowuję tekst…")
    text = fetch_text(SRC_URL)
    print("▶ Tokenizuję słowa…")
    tokens = tokenize_pl_words(text)

    # lista wariantów (normalizacja × stopwords)
    variants = [
        ("none", False),
        ("none", True),
        ("stem_A", False),
        ("stem_A", True),
        ("stem_B", False),
        ("stem_B", True),
    ]
    if _morf is not None:
        variants += [("lemma", False), ("lemma", True)]

    # nagłówek raportu
    with OUT_TXT.open("w", encoding="utf-8") as rep:
        w = lambda s="": rep.write(s + "\n")

        # ======= STRONA TYTUŁOWA =======
        w("LALKA – ANALIZA N-GRAMÓW (1..4) – RAPORT")
        w(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        w(f"Źródło: {SRC_URL}")
        w("=" * 88)
        w("SPIS TREŚCI")
        w("  1. Ustawienia i warianty")
        w("  2. Wyniki wg wariantów (Top 20)")
        w("  3. Wskazówki interpretacyjne")
        w("=" * 88)
        w()

        # ======= 1. USTAWIENIA =======
        w("1. USTAWIENIA I WARIANTY")
        w("-" * 88)
        w(f"• Katalog wyników: {OUT_DIR.resolve()}")
        w(f"• TOP_K: {TOP_K}, N_MAX: {N_MAX}")
        w(
            f"• Stopwords: {'NLTK(polish)' if 'polish' in stopwords.fileids() else 'lista awaryjna'}"
        )
        w(f"• Morfeusz2: {'TAK' if _morf is not None else 'NIE (pomijam lematyzację)'}")
        w(
            "• Warianty normalizacji: none / stem_A / stem_B"
            + ("/ lemma" if _morf is not None else "")
        )
        w()

        # ======= 2. WYNIKI WG WARIANTÓW =======
        w("2. WYNIKI WG WARIANTÓW (Top 20 n-gramów)")
        w("-" * 88)

        for norm, rm_stop in variants:
            variant_title = (
                f"[normalizacja={norm} | stopwords={'REMOVE' if rm_stop else 'KEEP'}]"
            )
            w()
            w(variant_title)
            w("-" * len(variant_title))

            # przygotuj tokeny wg wariantu
            try:
                toks_norm = normalize(tokens, norm)
            except RuntimeError as e:
                w(f"(pomijam) {e}")
                continue

            toks_norm = [t for t in toks_norm if is_alpha_pl(t)]
            toks_used = remove_stopwords(toks_norm) if rm_stop else toks_norm

            for n in range(1, N_MAX + 1):
                grams = make_ngrams(toks_used, n)
                freq = Counter(grams)
                total = sum(freq.values())
                top = freq.most_common(TOP_K)
                rows = [(ng, c, (c / total * 100.0 if total else 0.0)) for ng, c in top]

                # sekcja w raporcie
                w(f"\n  • n = {n}  (liczba n-gramów: {total})")
                w(fmt_table(rows, widths=(6, 60, 10, 10)))

                # zapis CSV
                csv_name = (
                    OUT_DIR
                    / f"ngrams_n{n}__{norm}__{'remove' if rm_stop else 'keep'}.csv"
                )
                with csv_name.open("w", newline="", encoding="utf-8") as cf:
                    cw = csv.writer(cf)
                    cw.writerow(["ngram", "count", "share"])
                    for ng, c in top:
                        share = (c / total) if total else 0.0
                        cw.writerow([ng, c, round(share, 6)])

        # ======= 3. WSKAZÓWKI INTERPRETACYJNE =======
        w()
        w("3. WSKAZÓWKI INTERPRETACYJNE")
        w("-" * 88)
        w("• 'none + keep' – 1- i 2-gramy zdominują słowa funkcyjne (i, w, na...).")
        w(
            "• Usunięcie stopwords ('remove') odsłania treściowe kolokacje (nazwiska, miejsca, związki rzeczownikowe)."
        )
        w(
            "• 'stem_A' / 'stem_B' – proste obcinanie końcówek w polskim bywa destabilizujące (artefakty rdzeni)."
        )
        w(
            "• 'lemma' (Morfeusz2) – scala odmiany do form słownikowych → stabilniejsze i sensowniejsze n-gramy."
        )
        w("=" * 88)
        w("KONIEC RAPORTU")

    print(f"✅ Zrobione. Raport: {OUT_TXT}")
    print(f"   CSV: {OUT_DIR / 'ngrams_n{1..4}__{norm}__{keep|remove}.csv'}")


# ========== START ==========
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("❌ Błąd krytyczny:", repr(e))
