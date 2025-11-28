import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def clean_text(text):
    """Clean and preprocess text data"""
    text = str(text).lower()
    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return text


# Read and preprocess the training data
df = pd.read_csv(
    "sentiment/train.csv", encoding="latin-1"
)  # Changed encoding to latin-1
df["cleaned_text"] = df["text"].apply(clean_text)

# Prepare data for sentiment classification
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["cleaned_text"])
y = df["sentiment"]

# Split data for training and validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train sentiment classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate model
val_predictions = model.predict(X_val)
print("Model Performance:")
print(f"Accuracy: {accuracy_score(y_val, val_predictions):.3f}")
print("\nClassification Report:")
print(classification_report(y_val, val_predictions))

# 1. Basic sentiment distribution
sentiment_dist = df["sentiment"].value_counts()
print("\nSentiment Distribution:")
print(sentiment_dist)
print("\nPercentages:")
print(sentiment_dist / len(df) * 100)

# 2. Average text length by sentiment
df["text_length"] = df["text"].str.len()
avg_length = df.groupby("sentiment")["text_length"].mean()
print("\nAverage Text Length by Sentiment:")
print(avg_length)

# 3. Analyze patterns by metadata
print("\nSentiment Distribution by Time of Day:")
time_sentiment = pd.crosstab(df["Time of Tweet"], df["sentiment"])
print(time_sentiment)

print("\nSentiment Distribution by Age Group:")
age_sentiment = pd.crosstab(df["Age of User"], df["sentiment"])
print(age_sentiment)

# 4. Create visualizations

# Create a figure with multiple subplots
plt.figure(figsize=(20, 15))

# 1. Sentiment distribution (pie chart)
plt.subplot(2, 2, 1)
plt.pie(
    sentiment_dist,
    labels=sentiment_dist.index,
    autopct="%1.1f%%",
    colors=["lightcoral", "lightblue", "lightgreen"],
)
plt.title("Sentiment Distribution", pad=20, size=14)

# 2. Average text length by sentiment (bar plot)
plt.subplot(2, 2, 2)
avg_length.plot(kind="bar", color=["lightcoral", "lightblue", "lightgreen"])
plt.title("Average Text Length by Sentiment", pad=20, size=14)
plt.xlabel("Sentiment")
plt.ylabel("Characters")
plt.xticks(rotation=45)

# 3. Time of day sentiment distribution (stacked bar chart)
plt.subplot(2, 2, 3)
time_sentiment_pct = time_sentiment.div(time_sentiment.sum(axis=1), axis=0) * 100
time_sentiment_pct.plot(
    kind="bar", stacked=True, color=["lightcoral", "lightblue", "lightgreen"]
)
plt.title("Sentiment Distribution by Time of Day (%)", pad=20, size=14)
plt.xlabel("Time of Day")
plt.ylabel("Percentage")
plt.legend(title="Sentiment")
plt.xticks(rotation=45)

# 4. Age group sentiment distribution (stacked bar chart)
plt.subplot(2, 2, 4)
age_sentiment_pct = age_sentiment.div(age_sentiment.sum(axis=1), axis=0) * 100
age_sentiment_pct.plot(
    kind="bar", stacked=True, color=["lightcoral", "lightblue", "lightgreen"]
)
plt.title("Sentiment Distribution by Age Group (%)", pad=20, size=14)
plt.xlabel("Age Group")
plt.ylabel("Percentage")
plt.legend(title="Sentiment")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("sentiment_analysis_summary.png", dpi=300, bbox_inches="tight")

# Create separate heatmaps
plt.figure(figsize=(12, 5))

# 1. Time of day heatmap
plt.subplot(1, 2, 1)
sns.heatmap(time_sentiment, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Sentiment Count by Time of Day", pad=20)

# 2. Age group heatmap
plt.subplot(1, 2, 2)
sns.heatmap(age_sentiment, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Sentiment Count by Age Group", pad=20)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("sentiment_heatmaps.png", dpi=300, bbox_inches="tight")

# Save results to a text file
with open("english_sentiment_analysis.txt", "w") as f:
    f.write("Sentiment Analysis Results\n")
    f.write("========================\n\n")

    f.write("Sentiment Distribution:\n")
    f.write(str(sentiment_dist))
    f.write("\n\nPercentages:\n")
    f.write(str(sentiment_dist / len(df) * 100))

    f.write("\n\nAverage Text Length by Sentiment:\n")
    f.write(str(avg_length))

    f.write("\n\nSentiment Distribution by Time of Day:\n")
    f.write(str(time_sentiment))

    f.write("\n\nSentiment Distribution by Age Group:\n")
    f.write(str(age_sentiment))
