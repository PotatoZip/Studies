#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from stop_words import get_stop_words
import nltk

nltk.download("punkt_tab")


def remove_stopwords(input_file, output_file):
    """
    Remove Polish stopwords from a text file using stop-words library.

    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output text file
    """
    try:
        # Get Polish stopwords
        polish_stopwords = set(get_stop_words("polish"))

        # Also get common Polish stopwords manually to ensure coverage
        additional_polish_stopwords = {
            "oraz",
            "lecz",
            "gdyby",
            "więc",
            "czyli",
            "albo",
            "bądź",
            "tuż",
            "gdzie",
            "kiedy",
            "dlaczego",
            "jak",
            "czy",
            "jakie",
            "który",
            "która",
            "które",
            "tym",
            "tej",
            "tych",
            "tego",
            "tamtej",
            "tamte",
            "tamto",
            "tamtych",
            "nasz",
            "nasza",
            "nasze",
            "naszego",
            "naszej",
            "naszym",
            "naszymi",
            "i",
            "za",
            "tą",
            "tego",
            "w",
            "do",
            "oraz",
            "a",
            "lub",
            "z",
            "o",
            "u",
            "ale",
            "był",
            "było",
            "byli",
            "że",
            "ze",
            "przez",
            "tylko",
            "sobie",
            "przy",
        }

        # Combine both sets
        all_stopwords = polish_stopwords.union(additional_polish_stopwords)

        print(f"Loaded {len(all_stopwords)} Polish stopwords")

    except Exception as e:
        print(f"Error loading stopwords: {e}")
        return

    # Read the input file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Input file {input_file} not found!")
        return

    # Tokenize: split into words and convert to lowercase
    # Keep only alphabetic characters and remove punctuation
    words = nltk.word_tokenize(text.lower())

    print(f"Original text has {len(words)} words")

    # Filter out stopwords
    filtered_words = [word for word in words if word not in all_stopwords]

    print(f"After removing stopwords: {len(filtered_words)} words")
    print(f"Removed {len(words) - len(filtered_words)} stopwords")

    # Join words back into text with spaces
    clean_text = " ".join(filtered_words)

    # Write to output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(clean_text)
        print(f"Clean text saved to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")


def show_sample_stopwords_removed(input_file, num_samples=10):
    """
    Show a sample of words that would be removed as stopwords.
    """
    try:
        polish_stopwords = set(get_stop_words("polish"))

        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        words = re.findall(r"\b[a-ząćęłńóśźż]+\b", text.lower())
        removed_words = [word for word in words if word in polish_stopwords]

        print(
            f"\nSample of {min(num_samples, len(set(removed_words)))} stopwords being removed:"
        )
        for word in list(set(removed_words))[:num_samples]:
            print(f"  - {word}")

    except Exception as e:
        print(f"Error showing samples: {e}")


if __name__ == "__main__":
    input_file = "Dostojewski.txt"
    output_file = "Dostojewski_no_stopwords.txt"

    print("Removing Polish stopwords from training.txt...")

    # Show sample of what will be removed
    show_sample_stopwords_removed(input_file)

    # Remove stopwords
    remove_stopwords(input_file, output_file)
