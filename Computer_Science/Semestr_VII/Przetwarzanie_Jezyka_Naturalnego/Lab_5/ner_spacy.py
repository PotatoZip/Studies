import spacy
from pathlib import Path
import requests
from collections import Counter

MODEL = "en_core_web_md"
URL = "https://www.gutenberg.org/files/1524/1524-0.txt"
RAW_TXT = "hamlet.txt"


def download_txt(url: str, filename: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    response.encoding = "utf-8"
    Path(filename).write_text(response.text, encoding="utf-8")
    print(f"✓ Pobrano {filename}")
    return response.text


def main():
    nlp = spacy.load(MODEL)

    # Wczytaj tekst
    if Path(RAW_TXT).exists():
        text = Path(RAW_TXT).read_text(encoding="utf-8")
        print(f"✓ Wczytano lokalny plik {RAW_TXT}")
    else:
        text = download_txt(URL, RAW_TXT)

    # Analiza językowa
    doc = nlp(text)

    # Wyodrębnij byty nazwane
    ents = [(ent.text, ent.label_) for ent in doc.ents]
    total = len(ents)

    # Policz typy bytów
    counts = Counter(label for _, label in ents)

    # Przygotuj przykłady
    examples = {}
    for label in list(counts.keys())[:3]:
        examples[label] = [ent.text for ent in doc.ents if ent.label_ == label][:5]

    print("\n" + "=" * 50)
    print("   📘 PODSUMOWANIE ANALIZY NER (spaCy)")
    print("=" * 50)
    print(f"Przetworzono tekst: {RAW_TXT}")
    print(f"Liczba rozpoznanych bytów nazwanych: {total}")
    print(f"Liczba różnych typów bytów: {len(counts)}\n")

    print("Najczęstsze typy nazw własnych:")
    for label, cnt in counts.most_common(5):
        print(f"  - {label:<10} : {cnt}")

    print("\nPrzykładowe byty:")
    for label, sample_list in examples.items():
        print(f"  {label:<10}: {', '.join(sample_list)}")

    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
