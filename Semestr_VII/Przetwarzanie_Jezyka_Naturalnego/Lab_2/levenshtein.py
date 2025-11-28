import textdistance

sentence_1 = "Ala ma kota"
sentence_2 = "Ala posiada kota"

# Create output file
output_file = "distance_analysis_results.txt"
results = []


def add_result(text):
    """Add text to results list and print it"""
    print(text)
    results.append(text)


add_result("Comparing sentences:")
add_result(f"Sentence 1: '{sentence_1}'")
add_result(f"Sentence 2: '{sentence_2}'")
add_result("=" * 60)

# 1. LEVENSHTEIN DISTANCE
levenshtein_dist = textdistance.levenshtein(sentence_1, sentence_2)
levenshtein_norm = textdistance.levenshtein.normalized_similarity(
    sentence_1, sentence_2
)
add_result("\n1. LEVENSHTEIN DISTANCE")
add_result(
    "   How it works: Minimum number of single-character edits (insertions, deletions, substitutions)"
)
add_result("   to transform one string into another.")
add_result(f"   Distance: {levenshtein_dist}")
add_result(f"   Normalized similarity: {levenshtein_norm:.3f}")

# 2. HAMMING DISTANCE
hamming_dist = textdistance.hamming(sentence_1, sentence_2)
hamming_norm = textdistance.hamming.normalized_similarity(sentence_1, sentence_2)
add_result("\n2. HAMMING DISTANCE")
add_result(
    "   How it works: Number of positions where characters differ (strings must be same length)"
)
add_result(f"   Distance: {hamming_dist}")
add_result(f"   Normalized similarity: {hamming_norm:.3f}")
add_result("   Explanation: Compares character by character, counts mismatches")

# 3. JARO-WINKLER DISTANCE
jaro_winkler_sim = textdistance.jaro_winkler(sentence_1, sentence_2)
add_result("\n3. JARO-WINKLER SIMILARITY")
add_result(
    "   How it works: Based on matching characters and transpositions, with bonus for common prefixes"
)
add_result(f"   Similarity: {jaro_winkler_sim:.3f}")
add_result(
    "   Explanation: High similarity due to common prefix 'Ala' and suffix 'kota'"
)

# 4. JACCARD DISTANCE (character-based)
jaccard_sim = textdistance.jaccard(sentence_1, sentence_2)
add_result("\n4. JACCARD SIMILARITY (character-based)")
add_result(
    "   How it works: Size of intersection divided by size of union of character sets"
)
add_result(f"   Similarity: {jaccard_sim:.3f}")
add_result("   Explanation: Based on unique characters shared between strings")

# 5. COSINE SIMILARITY
cosine_sim = textdistance.cosine(sentence_1, sentence_2)
add_result("\n5. COSINE SIMILARITY")
add_result("   How it works: Cosine of angle between character frequency vectors")
add_result(f"   Similarity: {cosine_sim:.3f}")
add_result(
    "   Explanation: Measures similarity based on character frequency distributions"
)

# 6. SORENSEN-DICE COEFFICIENT
sorensen_sim = textdistance.sorensen_dice(sentence_1, sentence_2)
add_result("\n6. SORENSEN-DICE SIMILARITY")
add_result("   How it works: 2 * |intersection| / (|set1| + |set2|)")
add_result(f"   Similarity: {sorensen_sim:.3f}")
add_result("   Explanation: Emphasizes common elements more than Jaccard")

add_result("\n" + "=" * 60)
add_result("COMPARISON SUMMARY:")
add_result(f"Levenshtein distance: {levenshtein_dist} (lower = more similar)")
add_result(f"Levenshtein similarity: {levenshtein_norm:.3f} (higher = more similar)")
add_result(f"Hamming similarity: {hamming_norm:.3f}")
add_result(f"Jaro-Winkler similarity: {jaro_winkler_sim:.3f}")
add_result(f"Jaccard similarity: {jaccard_sim:.3f}")
add_result(f"Cosine similarity: {cosine_sim:.3f}")
add_result(f"Sorensen-Dice similarity: {sorensen_sim:.3f}")

add_result("\nANALYSIS:")
add_result("- Levenshtein shows exact edit operations needed")
add_result("- Jaro-Winkler gives highest similarity due to common prefix/suffix")
add_result(
    "- Character-based measures (Jaccard, Cosine, Sorensen) focus on character overlap"
)
add_result("- Hamming works but is less suitable for strings of different lengths")

add_result("\n" + "=" * 60)
add_result("WORD-LEVEL ANALYSIS:")

# Split sentences into words for word-level comparison
words_1 = sentence_1.split()
words_2 = sentence_2.split()

add_result(f"Words in sentence 1: {words_1}")
add_result(f"Words in sentence 2: {words_2}")

# Word-level Levenshtein
word_levenshtein = textdistance.levenshtein(words_1, words_2)
word_levenshtein_norm = textdistance.levenshtein.normalized_similarity(words_1, words_2)

# Word-level Jaccard
word_jaccard = textdistance.jaccard(words_1, words_2)

# Word-level Jaro-Winkler
word_jaro_winkler = textdistance.jaro_winkler(words_1, words_2)

add_result(f"\nWord-level Levenshtein distance: {word_levenshtein}")
add_result(f"Word-level Levenshtein similarity: {word_levenshtein_norm:.3f}")
add_result(f"Word-level Jaccard similarity: {word_jaccard:.3f}")
add_result(f"Word-level Jaro-Winkler similarity: {word_jaro_winkler:.3f}")

add_result("\nWORD-LEVEL EXPLANATION:")
add_result("- Need to substitute 'ma' with 'posiada' (1 word operation)")
add_result("- Word-level analysis shows structural similarity better")
add_result("- 2 out of 3 words are identical ('Ala', 'kota')")

add_result("\n" + "=" * 60)
add_result("DETAILED LEVENSHTEIN ANALYSIS:")
add_result("Character-by-character transformation:")
add_result("'Ala ma kota' -> 'Ala posiada kota'")
add_result("1. Keep 'Ala '")
add_result(
    "2. Replace 'ma' with 'posiada' (substitute 'm' with 'p', substitute 'a' with 'o', insert 's', insert 'i', insert 'a', insert 'd', insert 'a')"
)
add_result("3. Keep ' kota'")
add_result("Total: 6 operations (2 substitutions + 4 insertions)")

# Save results to file
with open(output_file, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")

print(f"\n\nResults saved to: {output_file}")
print(f"Total lines written: {len(results)}")
