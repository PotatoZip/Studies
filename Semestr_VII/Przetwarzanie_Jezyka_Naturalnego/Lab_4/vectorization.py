import argparse
import os
import re
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    StratifiedKFold,
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    auc,
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# --- NLTK ---
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

# --- gensim ---
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import Word2Vec


# ======================
#  NLTK: zasoby
# ======================
def ensure_nltk():
    """Zapewnia obecność zasobów NLTK."""
    to_check = [
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("corpora/omw-1.4", "omw-1.4"),
    ]
    for path, pkg in to_check:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)

    # Tagger
    try:
        nltk.data.find("taggers/averaged_perceptron_tagger_eng")
    except LookupError:
        try:
            nltk.download("averaged_perceptron_tagger_eng", quiet=True)
        except Exception:
            pass

    try:
        nltk.data.find("taggers/averaged_perceptron_tagger")
    except LookupError:
        nltk.download("averaged_perceptron_tagger", quiet=True)

# ======================
#  Preprocessing
# ======================
CUSTOM_STOP = {
    "escapenumber", "escapelength", "escapelink", "escapelng", "escapelon", "escapelong",
    "unsubscribe", "copyright", "privacy", "mailto", "html", "http", "https", "www",
    "com", "org", "net", "email", "e-mail", "click", "here",
}

def _wordnet_pos(treebank_tag):
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def safe_pos_tag(tokens):
    """POS-tag zgodny z NLTK 3.8+."""
    from nltk import pos_tag
    try:
        return pos_tag(tokens, lang="eng")
    except TypeError:
        return pos_tag(tokens)


def clean_tokenize_lemmatize(text, stop_set, lemmatizer):
    """lower → czyszczenie → usunięcie stopwords → POS-lemmatization."""
    if not isinstance(text, str):
        text = "" if pd.isna(text) else str(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+|\S+@\S+", " ", text)
    text = re.sub(r"\bescape[a-z]*\b", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = text.split()
    full_stop = stop_set.union(CUSTOM_STOP)
    tokens = [t for t in tokens if 3 <= len(t) <= 30 and t not in full_stop]

    if not tokens:
        return []

    tags = safe_pos_tag(tokens)
    lemmas = [lemmatizer.lemmatize(tok, _wordnet_pos(pos)) for tok, pos in tags]
    return lemmas


# ======================
#  Doc2Vec helpers
# ======================
def train_doc2vec(token_sequences, vector_size=100, dm=1, epochs=30, window=5, seed=42, min_count=5):
    documents = [
        TaggedDocument(words=(toks if isinstance(toks, list) else []), tags=[i])
        for i, toks in enumerate(token_sequences)
    ]
    model = Doc2Vec(
        vector_size=vector_size,
        min_count=min_count,
        workers=4,
        dm=dm,
        epochs=epochs,
        window=window,
        negative=5,
        hs=0,
        seed=seed,
    )
    model.build_vocab(documents)
    model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
    return model


def infer_doc_vectors(model, token_seqs, vector_size=100, infer_epochs=50, alpha=0.025):
    """Inferowanie wektorów Doc2Vec."""
    X = np.zeros((len(token_seqs), vector_size), dtype=float)
    for i, toks in enumerate(token_seqs):
        if toks:
            X[i] = model.infer_vector(toks, alpha=alpha, epochs=infer_epochs)
    return X

# ======================
#  Word2Vec helpers
# ======================
def train_word2vec(token_sequence, vector_size=100, sg=1, epochs=30, window=5, seed=42, min_count=5):
    """Trenowanie Word2Vec (sg=1 dla Skip-gram, sg=0 dla CBOW)"""
    model = Word2Vec(
        sentences=token_sequence,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=4,
        sg=sg,
        epochs=epochs,
        negative=5,
        hs=0,
        seed=seed,
    )
    return model

def get_word2vec_document_vectors(model, token_seqs, vector_size=100, aggregation='mean'):
    """
    Konwersja dokumentów na wektory poprzez agregację wektorów słów.

    Metody agregacji:
        - 'mean': średnia wektorów słów (domyślna)
        - 'max': maksimum po każdym wymiarze
        - 'sum': suma wektorów słów
    """
    X = np.zeros((len(token_seqs), vector_size), dtype=float)

    for i, toks in enumerate(token_seqs):
        if not toks:
            continue

        word_vecs = []
        for word in toks:
            if word in model.wv:
                word_vecs.append(model.wv[word])

        if word_vecs:
            word_vecs = np.array(word_vecs)
            if aggregation == 'mean':
                X[i] = word_vecs.mean(axis=0)
            elif aggregation == 'max':
                X[i] = word_vecs.max(axis=0)
            elif aggregation == 'sum':
                X[i] = word_vecs.sum(axis=0)

    return X


# ======================
#  Normalizacja wektorów
# ======================
def normalize_vectors(X_train, X_test, method='standard'):
    """
    Normalizacja wektorów z użuciem wybranej strategii

    Metody:
        - 'standard': StandardScaler (zero mean, unit variance)
        - 'minmax': MinMaxScaler (zakres 0-1)
        - 'l2': normalizacja L2
        - 'none': brak normalizacji
    """
    if method == 'none':
        return X_train, X_test

    elif method == 'standard':
        scaler = StandardScaler()
        X_train_norm = scaler.fit_transform(X_train)
        X_test_norm = scaler.fit_transform(X_test)

    elif method == 'minmax':
        scaler = MinMaxScaler()
        X_train_norm = scaler.fit_transform(X_train)
        X_test_norm = scaler.fit_transform(X_test)

    elif method == 'l2':
        X_train_norm = X_train / (np.linalg(X_train, axis=1, keepidims=True) + 1e-8)
        X_test_norm = X_test / (np.linalg(X_test, axis=1, keepidims=True) + 1e-8)

    else:
        raise ValueError(f"Unknown normalization method: {method}")

    return X_train_norm, X_test_norm

# ======================
#  CV helper
# ======================
def make_adaptive_cv(y, max_splits=5, min_splits=2):
    """Zwraca StratifiedKFold z liczbą foldów ≤ liczebność klasy mniejszości."""
    _, counts = np.unique(y, return_counts=True)
    min_class = counts.min() if len(counts) else max_splits
    n_splits = max(min_splits, min(max_splits, int(min_class)))
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42), n_splits


# ======================
#  Ewaluacja i wykresy
# ======================
def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    y_score = None
    if hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        try:
            y_score = model.decision_function(X_test)
        except Exception:
            y_score = None

    fpr = tpr = roc_auc = None
    if y_score is not None and len(np.unique(y_test)) == 2:
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)

    return {
        "name": name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "cm": cm,
        "fpr": fpr,
        "tpr": tpr,
        "roc_auc": roc_auc,
    }


def plot_confusion_matrix(cm, title, out_path):
    plt.figure(figsize=(5, 5))
    plt.imshow(cm, interpolation="nearest", cmap='Blues')
    plt.title(title)
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.xticks([0, 1], ["Ham (0)", "Spam (1)"])
    plt.yticks([0, 1], ["Ham (0)", "Spam (1)"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j], ha="center", va="center", color='white' if cm[i,j] > cm.max()/2 else 'black')
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_roc(fpr, tpr, auc_val, title, out_path):
    if fpr is None or tpr is None:
        return
    plt.figure(figsize=(5, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc_val:.3f}", linewidth=2)
    plt.plot([0, 1], [0, 1], linestyle="--", color='gray')
    plt.title(title)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

# ======================
#  Main
# ======================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", type=str, required=True, help="Ścieżka do CSV (kolumny: label, text)")
    parser.add_argument("--out_dir", type=str, default="wyniki", help="Folder wyjściowy")
    parser.add_argument("--max_samples", type=int, default=83446, help="Limit próbek")
    parser.add_argument("--vector_size", type=int, default=200, help="Rozmiar wektora")
    parser.add_argument("--dm", type=int, default=1, choices=[0, 1], help="Doc2Vec dm: 1=PV-DM, 0=PV-DBOW")
    parser.add_argument("--sg", type=int, default=1, choices=[0, 1], help="Word2Vec sg: 1=Skip-gram, 0=CBOW")
    parser.add_argument("--d2v_epochs", type=int, default=30, help="Epoki Doc2Vec")
    parser.add_argument("--w2v_epochs", type=int, default=30, help="Epoki Word2Vec")
    parser.add_argument("--infer_epochs", type=int, default=50, help="Epoki inferencji Doc2Vec")
    parser.add_argument("--w2v_aggregation", type=str, default='mean', choices=['mean', 'max', 'sum'],
                        help="Metoda agregacji wektorów Word2Vec")
    parser.add_argument("--normalization", type=str, default='standard',
                        choices=['standard', 'minmax', 'l2', 'none'],
                        help="Metoda normalizacji wektorów")
    parser.add_argument("--random_iter", type=int, default=25, help="n_iter RandomizedSearch")
    parser.add_argument("--class_weight_balanced", action="store_true", help="Użyj class_weight='balanced'")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    warnings.filterwarnings("ignore")

    # NLTK zasoby
    ensure_nltk()
    stop_set = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    # Wczytanie danych
    print("Wczytywanie danych...")
    df = pd.read_csv(args.csv_path)
    df.columns = [c.lower() for c in df.columns]
    assert "label" in df.columns and "text" in df.columns, "CSV musi zawierać 'label' i 'text'."

    df = df.dropna(subset=["label", "text"]).reset_index(drop=True)
    df["label"] = df["label"].astype(int)
    df = df[df["label"].isin([0, 1])].reset_index(drop=True)

    if len(df) > args.max_samples:
        df = df.sample(n=args.max_samples, random_state=42).reset_index(drop=True)

    # Preprocessing
    print("Czyszczenie tekstu, lematyzacja...")
    df["tokens"] = df["text"].apply(lambda t: clean_tokenize_lemmatize(t, stop_set, lemmatizer))

    y = df["label"].values

    # =====================
    # EXPERIMENT 1: Doc2Vec
    # =====================
    print("\n" + "="*60)
    print("EXPERIMENT 1: Doc2Vec")
    print("="*60)

    print("Trening Doc2Vec...")
    d2v = train_doc2vec(
        df["tokens"].tolist(),
        vector_size=args.vector_size,
        dm=args.dm,
        epochs=args.d2v_epochs,
        window=5,
        seed=42,
        min_count=5,
    )

    print("Inferencja wektorów Doc2Vec...")
    X_d2v = infer_doc_vectors(
        d2v,
        df["tokens"].tolist(),
        vector_size=args.vector_size,
        infer_epochs=args.infer_epochs,
        alpha=0.025,
    )

    # Split i normalizacja
    X_train_d2v, X_test_d2v, y_train, y_test = train_test_split(
        X_d2v, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Normalizacja wektorów Doc2Vec ({args.normalization})...")
    X_train_d2v_norm, X_test_d2v_norm = normalize_vectors(X_train_d2v, X_test_d2v, args.normalization)

    # =====================
    # EXPERIMENT 2: Word2Vec
    # =====================
    print("\n" + "="*60)
    print("EXPERIMENT 2: Word2Vec")
    print("="*60)

    print("Trening Word2Vec...")
    w2v = train_word2vec(
        df["tokens"].tolist(),
        vector_size=args.vector_size,
        sg=args.sg,
        epochs=args.w2v_epochs,
        window=5,
        seed=42,
        min_count=5,
    )

    print(f"Generowanie wektorów Word2Vec (agregacja: {args.w2v_aggregation})...")
    X_w2v = get_word2vec_document_vectors(
        w2v,
        df["tokens"].tolist(),
        vector_size=args.vector_size,
        aggregation=args.w2v_aggregation
    )

    # Split i normalizacja
    X_train_w2v, X_test_w2v, _, _ = train_test_split(
        X_w2v, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Normalizacja wektorów Word2Vec ({args.normalization})...")
    X_train_w2v_norm, X_test_w2v_norm = normalize_vectors(X_train_w2v, X_test_w2v, args.normalization)

    # =====================
    # 5 Modeli klasyfikacji
    # =====================
    cv, n_splits = make_adaptive_cv(y_train, max_splits=5)
    print(f"\nCV folds: {n_splits}")

    class_weight = "balanced" if args.class_weight_balanced else None

    # Model 1: Logistic Regression
    log_reg = LogisticRegression(max_iter=10000, solver="saga", random_state=42, class_weight=class_weight)
    log_param = [
        {"penalty": ["l2"], "C": np.logspace(-3, 3, 15)},
        {"penalty": ["l1"], "C": np.logspace(-3, 3, 15)},
    ]

    # Model 2: LinearSVC
    svm = LinearSVC(random_state=42, class_weight=class_weight, max_iter=5000)
    svm_param = {
        "C": np.logspace(-3, 3, 15),
        "loss": ["hinge", "squared_hinge"],
    }

    # Model 3: Random Forest
    rf = RandomForestClassifier(
        random_state=42,
        n_jobs=-1,
        class_weight=("balanced_subsample" if args.class_weight_balanced else None),
    )
    rf_param = {
        "n_estimators": [100, 200, 400],
        "max_depth": [None, 10, 20, 40],
        "min_samples_split": [2, 5, 10],
        "max_features": ["sqrt", "log2"],
    }

    # Model 4: Gradient Boosting
    gb = GradientBoostingClassifier(random_state=42)
    gb_param = {
        "n_estimators": [100, 200, 300],
        "learning_rate": [0.01, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "subsample": [0.8, 1.0],
    }

    # Model 5: Naive Bayes
    nb = GaussianNB()
    nb_param = {
        "var_smoothing": np.logspace(-11, -7, 10)
    }

    models_config = [
        ("LogisticRegression", log_reg, log_param),
        ("LinearSVC", svm, svm_param),
        ("RandomForest", rf, rf_param),
        ("GradientBoosting", gb, gb_param),
        ("NaiveBayes", nb, nb_param),
    ]

    # =====================
    # Trening i ewaluacja
    # =====================
    all_results = []

    for vectorization_name, X_train_vec, X_test_vec in [
        ("Doc2Vec", X_train_d2v_norm, X_test_d2v_norm),
        ("Word2Vec", X_train_w2v_norm, X_test_w2v_norm),
    ]:
        print("\n" + "="*60)
        print(f"Wektoryzacja: {vectorization_name}")
        print("="*60)

        for model_name, model, param_dist in models_config:
            print(f"\nTuning {model_name}...")

            search = RandomizedSearchCV(
                model,
                param_dist,
                n_iter=args.random_iter,
                scoring="f1",
                cv=cv,
                random_state=42,
                n_jobs=-1,
                verbose=0,
            )

            search.fit(X_train_vec, y_train)
            print(f"Best params: {search.best_params_}")
            best_model = search.best_estimator_

            # Kalibracja dla SVC
            if model_name == "LinearSVC":
                try:
                    calibrated = CalibratedClassifierCV(best_model, cv=min(n_splits, 3))
                    calibrated.fit(X_train_vec, y_train)
                    best_model = calibrated
                    model_name = "LinearSVC_cal"
                except Exception as e:
                    print(f"Kalibracja pominięta: {e}")

            # Ewaluacja
            full_name = f"{vectorization_name}_{model_name}"
            print(f"Ewaluacja: {full_name}")
            res = evaluate_model(full_name, best_model, X_test_vec, y_test)
            all_results.append(res)

            # Zapisz wykresy
            safe_name = full_name.replace(" ", "_").replace("(", "").replace(")", "")
            cm_path = out_dir / f"cm_{safe_name}.png"
            plot_confusion_matrix(res["cm"], f"Confusion Matrix — {full_name}", cm_path)

            if res["fpr"] is not None:
                roc_path = out_dir / f"roc_{safe_name}.png"
                plot_roc(res["fpr"], res["tpr"], res["roc_auc"], f"ROC — {full_name}", roc_path)

    # =====================
    # Podsumowanie wyników
    # =====================
    metrics_df = pd.DataFrame([
        {
            "model": r["name"],
            "accuracy": r["accuracy"],
            "precision": r["precision"],
            "recall": r["recall"],
            "f1": r["f1"],
            "roc_auc": r["roc_auc"] if r["roc_auc"] else 0.0,
        }
        for r in all_results
    ]).sort_values(by="f1", ascending=False)

    metrics_csv = out_dir / "metrics_comparison.csv"
    metrics_df.to_csv(metrics_csv, index=False)

    print("\n" + "="*60)
    print("FINAL RESULTS (sorted by F1-score)")
    print("="*60)
    print(metrics_df.to_string(index=False))
    print(f"\nPliki zapisane w: {out_dir.resolve()}")
    print(f"Metryki: {metrics_csv.name}")

    # Porównanie Doc2Vec vs Word2Vec
    print("\n" + "="*60)
    print("Doc2Vec vs Word2Vec Comparison")
    print("="*60)

    d2v_results = metrics_df[metrics_df['model'].str.startswith('Doc2Vec')]
    w2v_results = metrics_df[metrics_df['model'].str.startswith('Word2Vec')]

    print(f"\nDoc2Vec - średnia F1: {d2v_results['f1'].mean():.4f}")
    print(f"Word2Vec - średnia F1: {w2v_results['f1'].mean():.4f}")
    print(f"\nDoc2Vec - najlepszy model: {d2v_results.iloc[0]['model']} (F1: {d2v_results.iloc[0]['f1']:.4f})")
    print(f"Word2Vec - najlepszy model: {w2v_results.iloc[0]['model']} (F1: {w2v_results.iloc[0]['f1']:.4f})")


if __name__ == "__main__":
    main()
