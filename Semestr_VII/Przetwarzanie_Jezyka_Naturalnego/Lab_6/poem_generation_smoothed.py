import requests
import re
import random
import nltk
from nltk.lm import Laplace, KneserNeyInterpolated
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.tokenize import word_tokenize, sent_tokenize


def ensure_nltk_resources():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")


def download_text(url, encoding="utf-8"):
    r = requests.get(url)
    r.encoding = encoding
    return r.text


def clean_text_for_poems(text):
    # remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # remove common server artifacts and error snippets
    text = re.sub(r"nginx/[0-9\.]+", " ", text, flags=re.I)
    text = re.sub(r"404 not found", " ", text, flags=re.I)
    # remove leftover angle-bracket fragments and tags with spaces
    text = re.sub(r"<\s*/?\w+\s*>", " ", text)
    # remove URLs
    text = re.sub(r"https?://\S+", " ", text)
    # remove weird repeated punctuation sequences and control chars
    text = re.sub(r"\x0c", " ", text)
    # preserve paragraph/line breaks: normalize CRLF -> LF
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # collapse spaces and tabs but keep newlines
    text = re.sub(r"[ \t]+", " ", text)
    # collapse multiple newlines to at most two (paragraph separator)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # strip trailing/leading spaces on each line
    lines = [ln.strip() for ln in text.split("\n")]
    return "\n".join(lines).strip()


def extract_poems(text, min_length=3):
    # split by lines and collect blocks of short lines as poems
    lines = [l.strip() for l in text.splitlines()]
    poems = []
    block = []
    for line in lines:
        if not line:
            if block and len(block) >= min_length:
                poems.append(" ".join(block))
            block = []
            continue
        # skip metadata lines with all caps or headers
        if len(line) < 200:
            block.append(line)
        else:
            if block and len(block) >= min_length:
                poems.append(" ".join(block))
            block = []
    if block and len(block) >= min_length:
        poems.append(" ".join(block))
    return poems


def tokenize_corpus(text):
    sents = sent_tokenize(text.lower(), language="polish")
    tokenized = [word_tokenize(s, language="polish") for s in sents]
    # remove empty token lists
    return [t for t in tokenized if len(t) > 0]


paktofonika_style = (
    "życie to jest ulica gdzie każdy gra swoją rolę "
    "w głowie chaos a serce krwawi na pół "
    "słowa lecą jak kule prosto w cel "
    "twardy jest ten świat lecz ja wciąż gram swój rap "
    "wiem że czas ucieka jak woda przez dłoń "
    "ale stoję mocno z wiarą w sobie "
    "patrzę w niebo szukam swojej drogi "
    "muzyka jest moją bronią przeciw złu"
)


def train_and_generate(
    tokenized_sentences, n=3, models=None, seeds=None, poems_per_model=5
):
    if models is None:
        # Default: generate only Laplace and Kneser‑Ney
        models = {
            "Laplace": Laplace,
            "KneserNey": KneserNeyInterpolated,
        }

    results = {}

    # corpus vocabulary for fallback sampling (alphabetic tokens only)
    corpus_vocab = sorted(
        {w for sent in tokenized_sentences for w in sent if any(c.isalpha() for c in w)}
    )

    for name, Model in models.items():
        print(f"Training {name} model...")
        train_data, vocab = padded_everygram_pipeline(n, tokenized_sentences)
        model = Model(n)
        model.fit(train_data, vocab)

        poems = []
        for i, seed in enumerate(seeds, 1):
            print(f"Model={name} Seed#{i} start={seed}")
            # generate a poem: num_lines lines, each up to max_words
            poem_lines = []
            for line_idx in range(6):
                # generate up to 12 words per line
                try:
                    gen = list(
                        model.generate(
                            12,
                            text_seed=tuple(seed),
                            random_seed=random.randint(0, 2**32 - 1),
                        )
                    )
                except TypeError:
                    # some models accept list seed
                    gen = list(
                        model.generate(
                            12, text_seed=seed, random_seed=random.randint(0, 2**32 - 1)
                        )
                    )
                # keep raw for diagnostics, then filter padding tokens
                raw_gen = list(gen)
                gen = [w for w in gen if w not in ("<s>", "</s>")]
                if not gen:
                    # Try fallback: generate without seed
                    try:
                        fallback = list(
                            model.generate(12, random_seed=random.randint(0, 2**32 - 1))
                        )
                    except TypeError:
                        fallback = list(
                            model.generate(12, random_seed=random.randint(0, 2**32 - 1))
                        )
                    fallback = [w for w in fallback if w not in ("<s>", "</s>")]
                    if fallback:
                        print(
                            f"  Line {line_idx+1}: empty after filter, used fallback generation: {fallback}"
                        )
                        gen = fallback
                    else:
                        # Final fallback: random unigram from corpus_vocab
                        if corpus_vocab:
                            unig = [random.choice(corpus_vocab)]
                            print(f"  Line {line_idx+1}: fallback to unigram {unig}")
                            gen = unig
                        else:
                            # leave as empty short line marker
                            gen = ["..."]
                # join and stop at punctuation if present
                line = " ".join(gen)
                poem_lines.append(line)
                # update seed to last (n-1) tokens for next line
                seed = (
                    (seed + gen)[-(n - 1) :]
                    if isinstance(seed, tuple) or isinstance(seed, list)
                    else gen[-(n - 1) :]
                )

            poems.append("\n".join(poem_lines))

        results[name] = poems

    return results


def save_poems(results, prefix="wygenerowane_wiersze"):
    for model_name, poems in results.items():
        fname = f"{prefix}_{model_name}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"WYGENEROWANE WIERSZE - model: {model_name}\n")
            f.write("=" * 60 + "\n\n")
            for i, p in enumerate(poems, 1):
                f.write(f"WIERSZ {i}\n")
                f.write("-" * 40 + "\n")
                f.write(p + "\n\n")
        print(f"Saved: {fname}")


def main():
    ensure_nltk_resources()

    print("Downloading texts...")
    mickiewicz_url = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt"
    stachura_url = "https://wolnelektury.pl/media/book/txt/siekierezada.txt"

    m_text = download_text(mickiewicz_url)
    s_text = download_text(stachura_url)

    # clean downloaded texts from HTML/server artifacts
    m_text = clean_text_for_poems(m_text)
    s_text = clean_text_for_poems(s_text)

    # extract poems (use only first portions to keep runtime small)
    m_poems = extract_poems(m_text[:80000], min_length=3)
    s_poems = extract_poems(s_text[:80000], min_length=3)

    # build combined corpus
    combined = []
    # include first few poem blocks
    for p in m_poems[:20] + s_poems[:20]:
        combined.append(p)
    combined.append(paktofonika_style)

    combined_text = "\n".join(combined)
    tokenized = tokenize_corpus(combined_text)
    print(f"Tokenized sentences: {len(tokenized)}")

    # choose seeds: pick 5 sentence starts from corpus
    seeds = []
    for sent in tokenized[:50]:
        if len(sent) >= 2:
            seeds.append(sent[:2])
        if len(seeds) >= 5:
            break

    # train models and generate
    results = train_and_generate(tokenized, n=3, seeds=seeds, poems_per_model=5)

    save_poems(results, prefix="wygenerowane_wiersze")


if __name__ == "__main__":
    main()
