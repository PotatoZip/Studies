import spacy
from pathlib import Path
import requests

nlp = spacy.load("en_core_web_md")


def download_txt_file(url: str, filename: str):
    import requests

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # Wymuś UTF-8 – Gutenberg tak serwuje te pliki
        response.encoding = "utf-8"
        with open(filename, "w", encoding="utf-8", newline="") as f:
            f.write(response.text)
        print(f"File downloaded into {filename}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")


def format_token(t):
    return f"{t.text:<15} {t.pos_:<6} {t.dep_:<12}"


def main():
    book = download_txt_file(
        "https://www.gutenberg.org/files/1524/1524-0.txt", "hamlet.txt"
    )

    doc = nlp(book.strip())

    header = f"{'TOKEN':<15} {'POS':<6} {'DEP':<12}"
    print(header)
    print("-" * len(header))

    [print(format_token(token)) for token in doc]

    output_path = Path("parts_of_speech.txt")
    with open("parts_of_speech.txt", "w", encoding="utf-8", newline="") as f:
        f.write(header + "\n")
        f.write("-" * len(header) + "\n")
        for token in doc:
            f.write(format_token(token) + "\n")


if __name__ == "__main__":
    main()
