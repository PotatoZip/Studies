import spacy
from pathlib import Path

nlp = spacy.load("en_core_web_md")
example_text = """
We introduce a quantum neural network, QNN, that can represent labeled data, classical or quantum,
and be trained by supervised learning. The quantum circuit consists of a sequence of parameter
dependent unitary transformations which acts on an input quantum state. For binary classification
a single Pauli operator is measured on a designated readout qubit. The measured output is the quantum
neural network's predictor of the binary label of the input state. First we look at classifying classical
data sets which consist of n-bit strings with binary labels. The input quantum state is an n-bit computational
basis state corresponding to a sample string. We show how to design a circuit made from two qubit unitaries
that can correctly represent the label of any Boolean function of n bits. For certain label functions the circuit
is exponentially long. We introduce parameter dependent unitaries that can be adapted by supervised learning of labeled data.
We study an example of real world data consisting of downsampled images of handwritten digits each of which has been labeled
as one of two distinct digits.
"""

doc = nlp(example_text.strip())


def format_token(t):
    return f"{t.text:<15} {t.lemma:<20}"


header = f"{'TOKEN':<15} {'LEMMA':<20}"
print(header)
print("-" * len(header))

[print(format_token(token)) for token in doc]

output_path = Path("tokens.txt")
with output_path.open("w", encoding="utf-8") as f:
    f.write(header + "\n")
    f.write("-" * len(header) + "\n")
    for token in doc:
        f.write(format_token(token) + "\n")

doc_vector = doc.vector
token_vectors = [(t.text, t.vector) for t in doc]

vec_path = Path("doc_vector.txt")
vec_path.write_text(" ".join(map(str, doc_vector)), encoding="utf-8")
print(f"Document vector saved to {vec_path.resolve()}")
