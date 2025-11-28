"""
Comparative NLP Analysis of Hamlet from Project Gutenberg
Compares: Porter Stemmer vs Snowball Stemmer
Analyzes: Tokenization, Stemming, and Lemmatization techniques
Results saved to: hamlet_nlp_analysis_results.txt
"""

import requests
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer
import re
from collections import Counter
from datetime import datetime

# Open output file
output_file = "hamlet_nlp_analysis_results.txt"
f = open(output_file, 'w', encoding='utf-8')

def write(text):
    """Helper function to write to file"""
    f.write(text + "\n")

# Download required NLTK data
print("Downloading required NLTK data...")
write(f"NLP Analysis Report - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
write("="*80)
write("")
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Download Hamlet from Project Gutenberg
print("Downloading Hamlet from Project Gutenberg...")
url = "https://www.gutenberg.org/files/1524/1524-0.txt"
response = requests.get(url)
text = response.text

# Extract the main text
start_marker = "HAMLET, PRINCE OF DENMARK"
end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    hamlet_text = text[start_idx:end_idx]
else:
    hamlet_text = text

# Clean the text
hamlet_text = re.sub(r'\n+', ' ', hamlet_text)
hamlet_text = re.sub(r'\s+', ' ', hamlet_text)

# Tokenize into sentences
sentences = sent_tokenize(hamlet_text)
meaningful_sentences = [s for s in sentences if len(s.split()) > 8]
selected_sentences = meaningful_sentences[10:15]

write("\n" + "="*80)
write("SELECTED 5 SENTENCES FROM HAMLET")
write("="*80)
for i, sentence in enumerate(selected_sentences, 1):
    write(f"\n{i}. {sentence}")

# Initialize stemmers and lemmatizer
porter_stemmer = PorterStemmer()
snowball_stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()

write("\n\n" + "="*80)
write("DETAILED COMPARISON: PORTER vs SNOWBALL STEMMER")
write("="*80)

# Process each sentence with both stemmers
for i, sentence in enumerate(selected_sentences, 1):
    write(f"\n{'='*80}")
    write(f"SENTENCE {i}")
    write(f"{'='*80}")
    write(f"Original: {sentence}\n")

    # Tokenization
    tokens = word_tokenize(sentence)
    write(f"Tokens ({len(tokens)}): {tokens}\n")

    # Stemming comparison
    write(f"{'Token':<20} {'Porter Stem':<20} {'Snowball Stem':<20} {'Match?'}")
    write("-" * 80)

    porter_stems = []
    snowball_stems = []
    differences = []

    for token in tokens:
        porter = porter_stemmer.stem(token)
        snowball = snowball_stemmer.stem(token)
        porter_stems.append(porter)
        snowball_stems.append(snowball)

        match = "+" if porter == snowball else "- DIFFERENT"
        write(f"{token:<20} {porter:<20} {snowball:<20} {match}")

        if porter != snowball:
            differences.append((token, porter, snowball))

    if differences:
        write(f"\nFound {len(differences)} difference(s) between stemmers in this sentence")
    else:
        write(f"\nBoth stemmers produced identical results for this sentence")

# Statistical Analysis
write("\n\n" + "="*80)
write("STATISTICAL ANALYSIS: STEMMER COMPARISON")
write("="*80)

all_tokens = []
porter_diffs = []
snowball_diffs = []
both_same = []

for sentence in selected_sentences:
    tokens = word_tokenize(sentence)
    for token in tokens:
        if token.isalpha():  # Only analyze words
            all_tokens.append(token)
            porter = porter_stemmer.stem(token)
            snowball = snowball_stemmer.stem(token)

            if porter != snowball:
                porter_diffs.append((token, porter, snowball))
            else:
                both_same.append((token, porter))

write(f"\nTotal words analyzed: {len(all_tokens)}")
write(f"Porter & Snowball agree: {len(both_same)} ({len(both_same)/len(all_tokens)*100:.1f}%)")
write(f"Porter & Snowball differ: {len(porter_diffs)} ({len(porter_diffs)/len(all_tokens)*100:.1f}%)")

if porter_diffs:
    write("\nExamples where stemmers differ:")
    for token, porter, snowball in porter_diffs[:10]:
        write(f"  {token:<15} → Porter: {porter:<12} | Snowball: {snowball:<12}")

# Comprehensive comparison: Tokenization vs Stemming vs Lemmatization
write("\n\n" + "="*80)
write("COMPREHENSIVE COMPARISON: TOKENIZATION vs STEMMING vs LEMMATIZATION")
write("="*80)

sample_sentence = selected_sentences[0]
write(f"\nSample Sentence: {sample_sentence}\n")

tokens = word_tokenize(sample_sentence)
porter_stems = [porter_stemmer.stem(t) for t in tokens]
snowball_stems = [snowball_stemmer.stem(t) for t in tokens]
lemmas = [lemmatizer.lemmatize(t.lower()) for t in tokens]

write(f"{'Original Token':<20} {'Porter Stem':<15} {'Snowball Stem':<15} {'Lemma':<15}")
write("=" * 80)

for token, p_stem, s_stem, lemma in zip(tokens, porter_stems, snowball_stems, lemmas):
    write(f"{token:<20} {p_stem:<15} {s_stem:<15} {lemma:<15}")

# Vocabulary reduction analysis
write("\n\n" + "="*80)
write("VOCABULARY REDUCTION ANALYSIS")
write("="*80)

all_text_tokens = []
for sentence in selected_sentences:
    all_text_tokens.extend([t.lower() for t in word_tokenize(sentence) if t.isalpha()])

unique_tokens = len(set(all_text_tokens))
unique_porter = len(set([porter_stemmer.stem(t) for t in all_text_tokens]))
unique_snowball = len(set([snowball_stemmer.stem(t) for t in all_text_tokens]))
unique_lemmas = len(set([lemmatizer.lemmatize(t) for t in all_text_tokens]))

write(f"\nOriginal unique words: {unique_tokens}")
write(f"After Porter stemming: {unique_porter} (reduction: {(1-unique_porter/unique_tokens)*100:.1f}%)")
write(f"After Snowball stemming: {unique_snowball} (reduction: {(1-unique_snowball/unique_tokens)*100:.1f}%)")
write(f"After lemmatization: {unique_lemmas} (reduction: {(1-unique_lemmas/unique_tokens)*100:.1f}%)")

# Detailed technique analysis
write("\n\n" + "="*80)
write("ANALYTICAL SUMMARY OF TECHNIQUES")
write("="*80)

write("""
╔════════════════════════════════════════════════════════════════════════════╗
║                          1. TOKENIZATION                                   ║
╚════════════════════════════════════════════════════════════════════════════╝

Purpose: Splits text into individual units (tokens) - words, punctuation, etc.

Algorithm: NLTK's Punkt Tokenizer
- Uses unsupervised machine learning approach
- Identifies sentence boundaries and word boundaries
- Handles abbreviations, contractions, and special cases

Characteristics:
- Preserves original word forms
- Includes punctuation as separate tokens
- Foundation for all other NLP tasks
- Language-specific rules

Example: "Don't go!" → ["Do", "n't", "go", "!"]


╔════════════════════════════════════════════════════════════════════════════╗
║                     2. STEMMING - PORTER STEMMER                           ║
╚════════════════════════════════════════════════════════════════════════════╝

Purpose: Reduces words to root form by removing suffixes

Algorithm: Porter Stemmer (1980, Martin Porter)
- Rule-based approach with 5 steps
- Applies suffix stripping rules sequentially
- Fast and lightweight
- Language: Originally English

Characteristics:
- Very fast performance
- May produce non-words (e.g., "organization" → "organ")
- Aggressive stemming
- Cannot handle irregular words well
- Good for information retrieval

Examples:
- "running", "runs", "ran" → "run" (stem may not be accurate)
- "fishing", "fished", "fisher" → "fish"


╔════════════════════════════════════════════════════════════════════════════╗
║                    3. STEMMING - SNOWBALL STEMMER                          ║
╚════════════════════════════════════════════════════════════════════════════╝

Purpose: Improved stemming algorithm (Porter2)

Algorithm: Snowball Stemmer (2001, Martin Porter)
- Evolution of Porter Stemmer
- More aggressive and accurate
- Better handling of English irregularities
- Supports multiple languages

Characteristics:
- More accurate than Porter
- Better handles exceptions
- Still very fast
- Slightly more aggressive stemming
- Multilingual support

Differences from Porter:
- Better handling of -tion, -sion endings
- Improved treatment of -ly adverbs
- More consistent results


╔════════════════════════════════════════════════════════════════════════════╗
║                        4. LEMMATIZATION                                    ║
╚════════════════════════════════════════════════════════════════════════════╝

Purpose: Reduces words to dictionary base form (lemma)

Algorithm: WordNet Lemmatizer
- Uses morphological analysis
- Dictionary lookup in WordNet database
- Context-aware (with POS tagging)
- Returns valid words only

Characteristics:
- Always produces valid words
- More accurate than stemming
- Handles irregular forms (e.g., "better" → "good")
- Slower than stemming
- Requires lexical database
- Best for NLU tasks

Examples:
- "running", "runs", "ran" → "run" (needs POS tag for accuracy)
- "better" → "good" (with proper POS tag)
- "feet" → "foot"


╔════════════════════════════════════════════════════════════════════════════╗
║                         KEY COMPARISONS                                    ║
╚════════════════════════════════════════════════════════════════════════════╝

SPEED:
  Tokenization > Porter Stemmer > Snowball Stemmer > Lemmatization

ACCURACY:
  Lemmatization > Snowball Stemmer > Porter Stemmer > Tokenization

VOCABULARY REDUCTION:
  Porter Stemmer ≈ Snowball Stemmer > Lemmatization > Tokenization

USE CASES:
  * Tokenization: Required first step for all NLP
  * Porter Stemmer: Fast IR systems, search engines (legacy)
  * Snowball Stemmer: Modern search, text mining
  * Lemmatization: Text analysis, NLU, semantic applications

WHEN TO USE WHAT:
  -> Search engines: Snowball Stemmer (speed + accuracy balance)
  -> Text classification: Either stemmer (vocabulary reduction)
  -> Sentiment analysis: Lemmatization (preserves meaning)
  -> Information extraction: Lemmatization (accurate word forms)
  -> Real-time systems: Stemming (faster processing)
""")

write("\n" + "="*80)
write("ANALYSIS COMPLETE")
write("="*80)

# Close the file
f.close()
print(f"\n✓ Analysis complete! Results saved to: {output_file}")
print(f"  Open the file to view all comparisons and analysis.")
