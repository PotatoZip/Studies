from nltk.lm import MLE, KneserNeyInterpolated, Laplace
from nltk.lm.preprocessing import padded_everygram_pipeline

corpus = [
    ["Platon", "mieszkał", "w", "Atenach", "."],
    ["Sokrates", "mieszkał", "w", "Atenach", "."],
]

n = 3

models = {
    "MLE": MLE,
    "Laplace": Laplace,
    "KneserNey": KneserNeyInterpolated,
}

for name, Model in models.items():
    train_data_gen, vocab_gen = padded_everygram_pipeline(n, corpus)
    model = Model(n)
    model.fit(train_data_gen, vocab_gen)
    print(f"\n{name}: P('Atenach' | ['w']) = {model.score('Atenach', ['w'])}")
