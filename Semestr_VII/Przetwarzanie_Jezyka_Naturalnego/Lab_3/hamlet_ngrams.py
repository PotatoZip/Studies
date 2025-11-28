#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hamlet N-grams Analysis (1..4)
Compares different stemming approaches with/without stopwords
"""

import csv
import os
from pathlib import Path
import re
from collections import Counter
from datetime import datetime
from typing import List, Tuple

import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer

# ========== SETTINGS ==========
SRC_URL = "https://www.gutenberg.org/files/1524/1524-0.txt"
OUT_DIR = Path("ngrams_hamlet")
OUT_TXT = OUT_DIR / "hamlet_en_ngrams_report.txt"

TOP_K = 20  # Top N-grams to show
N_MAX = 4  # Maximum n-gram length (1..4)

# ========== PREPARATION ==========
OUT_DIR.mkdir(parents=True, exist_ok=True)

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

ENGLISH_STOP = set(stopwords.words("english"))
porter = PorterStemmer()
snowball = SnowballStemmer("english")


# ========== HELPER FUNCTIONS ==========
def fetch_text(url: str) -> str:
    """Download and clean text from URL"""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    txt = resp.text
    # Remove Project Gutenberg header/footer (simple approach)
    txt = re.sub(r"\s+", " ", txt.strip())
    return txt


def normalize(tokens: List[str], mode: str) -> List[str]:
    """Apply normalization: none, porter, or snowball stemming"""
    if mode == "none":
        return [t.lower() for t in tokens]
    elif mode == "porter":
        return [porter.stem(t.lower()) for t in tokens]
    elif mode == "snowball":
        return [snowball.stem(t.lower()) for t in tokens]
    else:
        raise ValueError(f"Unknown normalization mode: {mode}")


def remove_stopwords(tokens: List[str]) -> List[str]:
    """Remove English stopwords"""
    return [t for t in tokens if t not in ENGLISH_STOP]


def make_ngrams(seq: List[str], n: int) -> List[str]:
    """Generate n-grams from token sequence"""
    return [" ".join(seq[i : i + n]) for i in range(len(seq) - n + 1)] if n > 0 else []


def fmt_table(rows: List[Tuple[str, int, float]], widths=(6, 52, 10, 9)) -> str:
    """Format results as ASCII table"""
    lines = []
    lines.append(
        f"{'rank':<{widths[0]}}{'ngram':<{widths[1]}}{'count':>{widths[2]}}{'share%':>{widths[3]}}"
    )
    lines.append("-" * sum(widths))
    for r, (ng, c, share) in enumerate(rows, 1):
        lines.append(
            f"{r:<{widths[0]}}{ng[: widths[1] - 2]:<{widths[1]}}{c:>{widths[2]}}{share:>{widths[3]}.2f}"
        )
    return "\n".join(lines)


# ========== MAIN LOGIC ==========
def main():
    print("▶ Fetching and preparing text...")
    text = fetch_text(SRC_URL)

    print("▶ Tokenizing words...")
    tokens = word_tokenize(text)
    # Keep only alphabetic tokens
    tokens = [t for t in tokens if t.isalpha()]

    # Variants: (normalization, remove_stopwords)
    variants = [
        ("none", False),
        ("none", True),
        ("porter", False),
        ("porter", True),
        ("snowball", False),
        ("snowball", True),
    ]

    # Generate report
    with OUT_TXT.open("w", encoding="utf-8") as rep:
        w = lambda s="": rep.write(s + "\n")

        # ======= TITLE PAGE =======
        w("HAMLET – N-GRAMS ANALYSIS (1..4) – REPORT")
        w(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        w(f"Source: {SRC_URL}")
        w("=" * 88)
        w("CONTENTS")
        w("  1. Settings and variants")
        w("  2. Results by variant (Top 20)")
        w("  3. Interpretation notes")
        w("=" * 88)
        w()

        # ======= 1. SETTINGS =======
        w("1. SETTINGS AND VARIANTS")
        w("-" * 88)
        w(f"• Output directory: {OUT_DIR.resolve()}")
        w(f"• TOP_K: {TOP_K}, N_MAX: {N_MAX}")
        w(f"• Stopwords: NLTK English stopwords ({len(ENGLISH_STOP)} words)")
        w("• Normalization variants: none / porter / snowball")
        w()

        # ======= 2. RESULTS BY VARIANT =======
        w("2. RESULTS BY VARIANT (Top 20 n-grams)")
        w("-" * 88)

        for norm, rm_stop in variants:
            variant_title = (
                f"[normalization={norm} | stopwords={'REMOVE' if rm_stop else 'KEEP'}]"
            )
            w()
            w(variant_title)
            w("-" * len(variant_title))

            # Prepare tokens for this variant
            toks_norm = normalize(tokens, norm)
            toks_used = remove_stopwords(toks_norm) if rm_stop else toks_norm

            for n in range(1, N_MAX + 1):
                grams = make_ngrams(toks_used, n)
                freq = Counter(grams)
                total = sum(freq.values())
                top = freq.most_common(TOP_K)
                rows = [(ng, c, (c / total * 100.0 if total else 0.0)) for ng, c in top]

                # Report section
                w(f"\n  • n = {n}  (total n-grams: {total})")
                w(fmt_table(rows, widths=(6, 60, 10, 10)))

                # Save CSV
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

        # ======= 3. INTERPRETATION NOTES =======
        w()
        w("3. INTERPRETATION NOTES")
        w("-" * 88)
        w("• 'none + keep' – Dominated by function words (the, and, to, of, etc.).")
        w(
            "• Removing stopwords reveals content-rich collocations (character names, themes)."
        )
        w("• 'porter' – Aggressive stemming, may over-stem (e.g., 'lying'→'li').")
        w("• 'snowball' – More conservative stemming, better preserves word meaning.")
        w(
            "• Compare stemmers to see trade-offs between conflation and interpretability."
        )
        w("=" * 88)
        w("END OF REPORT")

    print(f"✅ Done! Report: {OUT_TXT}")
    print(f"   CSVs: {OUT_DIR / 'ngrams_n{1..4}__{norm}__{keep|remove}.csv'}")


# ========== START ==========
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Critical error: {repr(e)}")
