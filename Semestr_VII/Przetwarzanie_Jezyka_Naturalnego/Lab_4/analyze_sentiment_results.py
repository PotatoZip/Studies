import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("sentiment_results.csv")

# Count sentiment frequencies
sentiment_counts = df["sentiment"].value_counts()

# Calculate percentages
sentiment_percentages = sentiment_counts / len(df) * 100

# Print statistics
print("Sentiment Analysis Results:")
print("\nTotal texts analyzed:", len(df))
print("\nSentiment Distribution:")
for sentiment, count in sentiment_counts.items():
    percentage = sentiment_percentages[sentiment]
    print(f"{sentiment}: {count} texts ({percentage:.1f}%)")

# Create a pie chart
plt.figure(figsize=(10, 8))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%")
plt.title("Sentiment Distribution in Blog Content")
plt.savefig("sentiment_distribution.png")
plt.close()

# Analyze text lengths and sentiment
df["text_length"] = df["text"].str.len()
print("\nAverage Text Length by Sentiment:")
print(df.groupby("sentiment")["text_length"].mean().round(1))

# Find examples of each sentiment
print("\nExample texts for each sentiment:")
for sentiment in sentiment_counts.index:
    sample = df[df["sentiment"] == sentiment].iloc[0]
    print(f"\n{sentiment.upper()} example:")
    print(f"Text: {sample['selected_text'][:200]}...")
