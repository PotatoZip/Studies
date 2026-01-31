import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

# Sample documents (20+ documents about different topics)
sample_documents = [
    # Technology documents
    "Machine learning algorithms are revolutionizing artificial intelligence and data science.",
    "Deep neural networks require significant computational power and large datasets.",
    "Python is the most popular programming language for data science and AI.",
    "Cloud computing enables scalable software deployment and data storage.",
    "Cybersecurity is crucial for protecting digital systems and networks.",
    "Blockchain technology provides decentralized and secure transactions.",
    "Quantum computing promises exponential improvements in processing power.",
    "Software development requires version control and continuous integration.",
    "Database management systems store and retrieve structured data efficiently.",
    "API development enables seamless communication between different applications.",

    # Sports documents
    "Basketball requires teamwork, agility, and excellent shooting skills.",
    "Soccer is the world's most popular sport with billions of fans.",
    "Olympic athletes train for years to compete at the highest level.",
    "Marathon running demands endurance and mental toughness.",
    "Professional tennis players compete in grand slam tournaments worldwide.",
    "Swimming is an excellent full-body workout and competitive sport.",
    "Football teams strategize plays to score touchdowns and win games.",
    "Cricket matches can last several days in test format.",
    "Gymnastics combines strength, flexibility, and artistic performance.",
    "Cycling competitions test speed and stamina over long distances.",

    # Additional mixed documents
    "Athletes use data analytics to improve their training performance.",
    "Sports technology helps track player statistics and game metrics.",
]

def download_data():
    # List of URLs for the Project Gutenberg txt files
    urls = [
        "https://www.gutenberg.org/files/1342/1342-0.txt",
        "https://www.gutenberg.org/files/2701/2701-0.txt",
        "https://www.gutenberg.org/files/11/11-0.txt",
        "https://www.gutenberg.org/files/84/84-0.txt",
        "https://www.gutenberg.org/files/345/345-0.txt",
        "https://www.gutenberg.org/files/174/174-0.txt",
        "https://www.gutenberg.org/files/1661/1661-0.txt",
        "https://www.gutenberg.org/files/36/36-0.txt",
        "https://www.gutenberg.org/files/2600/2600-0.txt",
        "https://www.gutenberg.org/files/1184/1184-0.txt",
        "https://www.gutenberg.org/files/1400/1400-0.txt",
        "https://www.gutenberg.org/files/2554/2554-0.txt",
        "https://www.gutenberg.org/files/768/768-0.txt",
        "https://www.gutenberg.org/files/236/236-0.txt",
        "https://www.gutenberg.org/files/1727/1727-0.txt",
        "https://www.gutenberg.org/files/120/120-0.txt",
        "https://www.gutenberg.org/files/55/55-0.txt",
        "https://www.gutenberg.org/files/1497/1497-0.txt",
        "https://www.gutenberg.org/files/521/521-0.txt",
        "https://www.gutenberg.org/files/829/829-0.txt"
    ]

    for url in urls:
        filename = url.split("/")[-1]
        filepath = os.path.join("data", filename)
        try:
            print(f"Downloading {filename}...")
            response = requests.get(url)
            response.raise_for_status()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved to {filepath}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

def load_documents(data_dir='data'):
    """
    Load documents from a directory.
    If directory doesn't exist, use sample documents.
    """
    documents = []

    if os.path.exists(data_dir):
        print(f"Loading documents from '{data_dir}' directory...")
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                    documents.append(f.read())

        if documents:
            print(f"Loaded {len(documents)} documents from directory.")
            return documents

    print("Data directory not found. Using sample documents...")
    return sample_documents

def perform_lda(documents, n_topics=2, n_top_words=10):
    """
    Perform LDA topic modeling on documents.
    """
    print(f"\n{'='*60}")
    print(f"Performing LDA with {n_topics} topics")
    print(f"{'='*60}\n")

    # Create document-term matrix
    vectorizer = CountVectorizer(
        max_df=0.95,  # Ignore terms appearing in >95% of documents
        min_df=2,      # Ignore terms appearing in <2 documents
        stop_words='english'
    )

    doc_term_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()

    print(f"Vocabulary size: {len(feature_names)} words")
    print(f"Document-term matrix shape: {doc_term_matrix.shape}\n")

    # Perform LDA
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=20
    )

    lda.fit(doc_term_matrix)

    # Display topics
    print(f"Topics discovered:\n")
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-n_top_words:][::-1]
        top_words = [feature_names[i] for i in top_words_idx]
        print(f"Topic {topic_idx + 1}:")
        print(f"  {', '.join(top_words)}\n")

    # Show document-topic distribution
    doc_topic_dist = lda.transform(doc_term_matrix)

    print(f"\nDocument-Topic Distribution (first 5 documents):")
    print(f"{'-'*60}")
    for i in range(min(5, len(documents))):
        print(f"Document {i+1}:")
        print(f"  Preview: {documents[i][:60]}...")
        for topic_idx in range(n_topics):
            print(f"  Topic {topic_idx + 1}: {doc_topic_dist[i][topic_idx]:.3f}")
        print()

    return lda, vectorizer, doc_topic_dist

def main():
    """
    Main function to run the LDA topic modeling.
    """
    print("LDA Topic Modeling Script")
    print("="*60)

    # Download documents
    download_data()

    # Load documents
    documents = load_documents('data')

    if len(documents) < 20:
        print(f"Warning: Only {len(documents)} documents loaded. Recommend at least 20.")

    # Perform LDA with 2 topics
    lda, vectorizer, doc_topic_dist = perform_lda(documents, n_topics=2)

    print("\nTopic modeling complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
