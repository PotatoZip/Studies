import requests
import re
import nltk
from nltk import ngrams
from collections import Counter
import matplotlib.pyplot as plt

# Download required NLTK data if not already present
nltk.download("punkt", quiet=True)


def download_txt_file(url: str, filename: str):
    """
    Downloads a txt file from a URL and saves it to a local file.

    Args:
        url (str): The URL of the txt file.
        filename (str): The name of the local file to save the content to.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "w") as f:
            f.write(response.text)
        print(f"File downloaded into {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")


def load_and_clean_text(filename: str) -> str:
    """
    Loads text from a file and cleans it up.

    Args:
        filename (str): The name of the file to load.

    Returns:
        str: Cleaned text with lowercase letters and removed special characters.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        # Convert to lowercase
        text = text.lower()

        # Remove special characters, keep only letters and spaces
        text = re.sub(r"[^a-ząćęłńóśźż\s]", "", text)

        # Replace multiple spaces with single space
        text = re.sub(r"\s+", " ", text)

        # Strip leading and trailing whitespace
        text = text.strip()

        return text
    except IOError as e:
        print(f"Error reading file: {e}")
        return ""


def generate_ngrams(text: str, n: int) -> list:
    """
    Generate n-grams from text.

    Args:
        text (str): Input text.
        n (int): Size of n-grams (1 for unigrams, 2 for bigrams, 3 for trigrams).

    Returns:
        list: List of n-grams as tuples.
    """
    words = text.split()
    return list(ngrams(words, n))


def display_ngrams(ngrams_list: list, ngram_type: str, top_n: int = 10):
    """
    Display the most common n-grams.

    Args:
        ngrams_list (list): List of n-grams.
        ngram_type (str): Type of n-grams (for display purposes).
        top_n (int): Number of top n-grams to display.
    """
    counter = Counter(ngrams_list)
    print(f"\n{ngram_type.upper()}:")
    print(f"Total {ngram_type}: {len(counter)}")
    print(f"Top {top_n} most common {ngram_type}:")

    for i, (ngram, count) in enumerate(counter.most_common(top_n), 1):
        if len(ngram) == 1:
            print(f"{i:2d}. '{ngram[0]}' - {count} times")
        else:
            ngram_str = " ".join(ngram)
            print(f"{i:2d}. '{ngram_str}' - {count} times")


def create_histogram(ngrams_list: list, ngram_type: str, top_n: int = 10):
    """
    Create a histogram of the most frequent n-grams.

    Args:
        ngrams_list (list): List of n-grams.
        ngram_type (str): Type of n-grams (for display purposes).
        top_n (int): Number of top n-grams to display.
    """
    counter = Counter(ngrams_list)
    top_ngrams = counter.most_common(top_n)

    if not top_ngrams:
        print(f"No {ngram_type} found to create histogram.")
        return

    # Prepare data for plotting
    labels = []
    counts = []

    for ngram, count in top_ngrams:
        if len(ngram) == 1:
            labels.append(ngram[0])
        else:
            labels.append(" ".join(ngram))
        counts.append(count)

    # Create the histogram
    plt.figure(figsize=(12, 8))
    bars = plt.bar(
        range(len(labels)), counts, color="skyblue", edgecolor="navy", alpha=0.7
    )

    # Customize the plot
    plt.title(
        f"Top {top_n} Most Frequent {ngram_type.capitalize()}",
        fontsize=16,
        fontweight="bold",
    )
    plt.xlabel("N-grams", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")

    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + height * 0.01,
            f"{counts[i]}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the plot
    filename = f"{ngram_type}_histogram_no_stopwords.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"Histogram saved as {filename}")

    # Display the plot
    plt.show()


def main():
    # Download file if needed (uncomment if you want to download)
    # url = "https://wolnelektury.pl/media/book/txt/dostojewski-wspomnienia-z-martwego-domu.txt"
    # filename = "Dostojewski.txt"
    # download_txt_file(url, filename)

    # Load and clean text from training.txt
    filename = "Dostojewski_no_stopwords.txt"
    print(f"Loading and cleaning text from {filename}...")

    cleaned_text = load_and_clean_text(filename)
    if not cleaned_text:
        print("No text to process.")
        return

    print(f"Text loaded successfully. Length: {len(cleaned_text)} characters")
    print(f"Number of words: {len(cleaned_text.split())}")

    # Generate unigrams
    unigrams = generate_ngrams(cleaned_text, 1)
    display_ngrams(unigrams, "unigrams")

    # Generate bigrams
    bigrams = generate_ngrams(cleaned_text, 2)
    display_ngrams(bigrams, "bigrams")

    # Generate trigrams
    trigrams = generate_ngrams(cleaned_text, 3)
    display_ngrams(trigrams, "trigrams")

    # Create histograms
    print("\nCreating histograms...")
    create_histogram(unigrams, "unigrams")
    create_histogram(bigrams, "bigrams")
    create_histogram(trigrams, "trigrams")


if __name__ == "__main__":
    main()
