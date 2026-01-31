import re
from collections import Counter
import matplotlib.pyplot as plt


def find_proper_nouns(text: str) -> list:
    """
    Find proper nouns in Polish text using regex.
    Looks for capitalized words that are not at the beginning of sentences.

    Args:
        text (str): Input text to analyze

    Returns:
        list: List of proper nouns found
    """
    # Pattern to find capitalized words that are not at sentence start
    # Look for words that are preceded by lowercase letters or certain punctuation
    # but not by sentence-ending punctuation (., !, ?)

    proper_nouns = []

    # Pattern 1: Words preceded by lowercase letters and space
    pattern1 = r"(?<=[a-ząćęłńóśźż])\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]{2,})"
    proper_nouns.extend(re.findall(pattern1, text))

    # Pattern 2: Words after commas, semicolons, colons, dashes
    pattern2 = r"(?<=[,:;—])\s+([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]{2,})"
    proper_nouns.extend(re.findall(pattern2, text))

    # Pattern 3: Words after common prepositions (fixed-width lookbehind)
    prepositions = [
        "w ",
        "z ",
        "na ",
        "do ",
        "od ",
        "i ",
        "a ",
        "po ",
        "za ",
        "o ",
        "u ",
    ]
    for prep in prepositions:
        pattern = f"(?<={prep})([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]{{2,}})"
        proper_nouns.extend(re.findall(pattern, text))

    # Filter out common words that might be capitalized but aren't proper nouns
    # and words that are too short
    filtered_nouns = []
    common_words = {
        "Ten",
        "Ta",
        "To",
        "Ale",
        "Lub",
        "Oraz",
        "Może",
        "Już",
        "Gdy",
        "Jak",
        "Czy",
        "Lub",
        "Jest",
        "Była",
        "Było",
        "Były",
        "Będzie",
        "Można",
        "Trzeba",
        "Wiele",
        "Jeden",
        "Jedna",
        "Jedno",
        "Dwa",
        "Trzy",
        "Każdy",
        "Każda",
        "Każde",
        "Inne",
        "Inna",
        "Inne",
        "Nie",
    }

    for noun in proper_nouns:
        if len(noun) >= 3 and noun not in common_words and not noun.isdigit():
            filtered_nouns.append(noun)

    return filtered_nouns


def analyze_proper_nouns(filename: str, top_n: int = 10):
    """
    Analyze proper nouns in text file and display results.

    Args:
        filename (str): Path to text file
        top_n (int): Number of top proper nouns to display
    """
    try:
        # Read the text file
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Analyzing proper nouns in {filename}...")
        print("-" * 50)

        # Find proper nouns
        proper_nouns = find_proper_nouns(text)

        if not proper_nouns:
            print("No proper nouns found.")
            return

        # Count frequencies
        noun_counter = Counter(proper_nouns)
        total_nouns = len(proper_nouns)
        unique_nouns = len(noun_counter)

        print(f"Total proper nouns found: {total_nouns}")
        print(f"Unique proper nouns: {unique_nouns}")
        print(f"\nTop {top_n} most frequent proper nouns:")
        print("-" * 40)

        top_nouns = noun_counter.most_common(top_n)

        for i, (noun, count) in enumerate(top_nouns, 1):
            percentage = (count / total_nouns) * 100
            print(f"{i:2d}. {noun:<15} - {count:2d} times ({percentage:.1f}%)")

        # Create histogram
        create_histogram(top_nouns, top_n)

        return noun_counter

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def create_histogram(top_nouns: list, top_n: int):
    """
    Create histogram of most frequent proper nouns.

    Args:
        top_nouns (list): List of (noun, count) tuples
        top_n (int): Number of top nouns
    """
    if not top_nouns:
        print("No data to create histogram.")
        return

    # Prepare data
    nouns = [noun for noun, count in top_nouns]
    counts = [count for noun, count in top_nouns]

    # Create histogram
    plt.figure(figsize=(12, 8))
    bars = plt.bar(
        range(len(nouns)), counts, color="lightcoral", edgecolor="darkred", alpha=0.8
    )

    # Customize plot
    plt.title(
        f"Top {top_n} Most Frequent Proper Nouns",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Proper Nouns", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    # Set x-axis labels
    plt.xticks(range(len(nouns)), nouns, rotation=45, ha="right")

    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.05,
            f"{counts[i]}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # Add grid for better readability
    plt.grid(axis="y", alpha=0.3)

    # Adjust layout
    plt.tight_layout()

    # Save plot
    filename = "proper_nouns_histogram.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"\nHistogram saved as {filename}")

    # Show plot
    plt.show()


def main():
    """Main function to run the proper nouns analysis."""
    input_file = "Dostojewski.txt"

    print("=== PROPER NOUNS ANALYSIS ===")
    print("Looking for capitalized words in the middle of sentences...")
    print("=" * 50)

    # Analyze proper nouns
    noun_counter = analyze_proper_nouns(input_file, top_n=10)

    if noun_counter:
        print(f"\nAll proper nouns found (showing first 20):")
        print("-" * 40)
        all_nouns = noun_counter.most_common(20)
        for noun, count in all_nouns:
            print(f"{noun}: {count}")


if __name__ == "__main__":
    main()
