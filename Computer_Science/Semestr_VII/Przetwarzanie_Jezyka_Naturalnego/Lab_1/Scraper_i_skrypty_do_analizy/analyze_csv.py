import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Usage: python analyze_csv.py <csv_file_path>
def main(csv_path):
    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    print("\nColumns:", list(df.columns))

    # Basic statistics
    print("\n--- Descriptive Statistics ---")
    print(df.describe(include='all'))

    # Mode
    print("\n--- Mode ---")
    print(df.mode().iloc[0])

    # Median
    print("\n--- Median ---")
    print(df.median(numeric_only=True))

    # Quartiles
    print("\n--- Quartiles ---")
    print(df.quantile([0.25, 0.5, 0.75]))

    # Min/Max
    print("\n--- Min ---")
    print(df.min(numeric_only=True))
    print("\n--- Max ---")
    print(df.max(numeric_only=True))

    # Histograms and Boxplots for numeric columns
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        plt.figure(figsize=(10,4))
        plt.subplot(1,2,1)
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f'Histogram of {col}')
        plt.subplot(1,2,2)
        sns.boxplot(x=df[col].dropna())
        plt.title(f'Boxplot of {col}')
        plt.tight_layout()
        plt.savefig(f'{col}_hist_box.png')
        plt.close()
        print(f"Saved histogram and boxplot for {col} as {col}_hist_box.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_csv.py <csv_file_path>")
    else:
        main(sys.argv[1])
