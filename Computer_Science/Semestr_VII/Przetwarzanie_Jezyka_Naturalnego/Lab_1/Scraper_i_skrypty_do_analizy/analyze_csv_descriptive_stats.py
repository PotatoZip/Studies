import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings

warnings.filterwarnings("ignore")

# Set style for better plots
try:
    plt.style.use("seaborn-v0_8")
except OSError:
    plt.style.use("seaborn")
sns.set_palette("husl")


def extract_numerical_data(df):
    """Extract and clean numerical data from the dataset"""
    numerical_data = {}

    # Price - already numerical
    if "price" in df.columns:
        prices = pd.to_numeric(df["price"], errors="coerce")
        numerical_data["price"] = prices.dropna()

    # Extract RAM in GB from spec_pami_ram
    if "spec_pami_ram" in df.columns:
        ram_values = []
        for ram_spec in df["spec_pami_ram"].fillna(""):
            if ram_spec and "GB" in str(ram_spec):
                # Extract number before GB
                import re

                match = re.search(r"(\d+)\s*GB", str(ram_spec))
                if match:
                    ram_values.append(int(match.group(1)))
                else:
                    ram_values.append(np.nan)
            else:
                ram_values.append(np.nan)
        numerical_data["ram_gb"] = pd.Series(ram_values).dropna()

    # Extract storage capacity from spec_pojemno_dysku_1
    if "spec_pojemno_dysku_1" in df.columns:
        storage_values = []
        for storage_spec in df["spec_pojemno_dysku_1"].fillna(""):
            if storage_spec and str(storage_spec).strip():
                # Extract number and convert to GB
                import re

                tb_match = re.search(r"(\d+(?:\.\d+)?)\s*TB", str(storage_spec))
                gb_match = re.search(r"(\d+)\s*GB", str(storage_spec))

                if tb_match:
                    storage_values.append(
                        float(tb_match.group(1)) * 1024
                    )  # Convert TB to GB
                elif gb_match:
                    storage_values.append(int(gb_match.group(1)))
                else:
                    storage_values.append(np.nan)
            else:
                storage_values.append(np.nan)
        numerical_data["storage_gb"] = pd.Series(storage_values).dropna()

    # Extract core count from spec_liczba_rdzeni
    if "spec_liczba_rdzeni" in df.columns:
        core_values = []
        for core_spec in df["spec_liczba_rdzeni"].fillna(""):
            if core_spec and str(core_spec).strip():
                import re

                match = re.search(r"(\d+)", str(core_spec))
                if match:
                    core_values.append(int(match.group(1)))
                else:
                    core_values.append(np.nan)
            else:
                core_values.append(np.nan)
        numerical_data["cores"] = pd.Series(core_values).dropna()

    return numerical_data


def calculate_descriptive_stats(data_series, name):
    """Calculate comprehensive descriptive statistics for a data series"""
    if len(data_series) == 0:
        return None

    stats = {
        "name": name,
        "count": len(data_series),
        "mean": data_series.mean(),
        "median": data_series.median(),
        "mode": (
            data_series.mode().iloc[0]
            if not data_series.mode().empty
            else "No unique mode"
        ),
        "min": data_series.min(),
        "max": data_series.max(),
        "std": data_series.std(),
        "variance": data_series.var(),
        "q1": data_series.quantile(0.25),  # First quartile
        "q3": data_series.quantile(0.75),  # Third quartile
        "iqr": data_series.quantile(0.75)
        - data_series.quantile(0.25),  # Interquartile range
        "range": data_series.max() - data_series.min(),
        "cv": (data_series.std() / data_series.mean())
        * 100,  # Coefficient of variation
        "skewness": data_series.skew(),
        "kurtosis": data_series.kurtosis(),
    }

    # Detect outliers using IQR method
    q1, q3 = stats["q1"], stats["q3"]
    iqr = stats["iqr"]
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data_series[(data_series < lower_bound) | (data_series > upper_bound)]
    stats["outlier_count"] = len(outliers)
    stats["outlier_percentage"] = (len(outliers) / len(data_series)) * 100

    return stats


def format_stats_table(stats_list):
    """Format statistics into a readable table"""
    if not stats_list:
        return "No numerical data found."

    # Create header
    table = "DESCRIPTIVE STATISTICS SUMMARY\n"
    table += "=" * 80 + "\n\n"

    # Column headers
    headers = ["Statistic", "Price (PLN)", "RAM (GB)", "Storage (GB)", "Cores"]
    available_cols = [s["name"] for s in stats_list if s]

    # Filter headers based on available data
    filtered_headers = ["Statistic"]
    filtered_stats = []

    for header in headers[1:]:
        col_name = header.split()[0].lower()
        if col_name == "price":
            matching_stats = next(
                (s for s in stats_list if s and "price" in s["name"].lower()), None
            )
        elif col_name == "ram":
            matching_stats = next(
                (s for s in stats_list if s and "ram" in s["name"].lower()), None
            )
        elif col_name == "storage":
            matching_stats = next(
                (s for s in stats_list if s and "storage" in s["name"].lower()), None
            )
        elif col_name == "cores":
            matching_stats = next(
                (s for s in stats_list if s and "cores" in s["name"].lower()), None
            )
        else:
            matching_stats = None

        if matching_stats:
            filtered_headers.append(header)
            filtered_stats.append(matching_stats)

    # Format table
    row_format = "{:<20} " + "{:<15} " * (len(filtered_headers) - 1) + "\n"
    table += row_format.format(*filtered_headers)
    table += "-" * 80 + "\n"

    # Statistical measures to include
    measures = [
        ("Count", "count"),
        ("Mean", "mean"),
        ("Median", "median"),
        ("Mode", "mode"),
        ("Min", "min"),
        ("Max", "max"),
        ("Std Dev", "std"),
        ("Q1 (25%)", "q1"),
        ("Q3 (75%)", "q3"),
        ("IQR", "iqr"),
        ("Range", "range"),
        ("CV (%)", "cv"),
        ("Skewness", "skewness"),
        ("Kurtosis", "kurtosis"),
        ("Outliers", "outlier_count"),
        ("Outlier %", "outlier_percentage"),
    ]

    for measure_name, measure_key in measures:
        row_values = [measure_name]
        for stats in filtered_stats:
            value = stats.get(measure_key, "N/A")
            if isinstance(value, (int, float)) and not np.isnan(value):
                if measure_key in [
                    "mean",
                    "median",
                    "min",
                    "max",
                    "std",
                    "variance",
                    "q1",
                    "q3",
                    "iqr",
                    "range",
                ]:
                    row_values.append(f"{value:.2f}")
                elif measure_key in ["cv", "outlier_percentage"]:
                    row_values.append(f"{value:.1f}")
                elif measure_key in ["skewness", "kurtosis"]:
                    row_values.append(f"{value:.3f}")
                else:
                    row_values.append(
                        str(
                            int(value)
                            if isinstance(value, float) and value.is_integer()
                            else value
                        )
                    )
            else:
                row_values.append(str(value))

        table += row_format.format(*row_values)

    return table


def create_distribution_plots(numerical_data, output_prefix):
    """Create distribution plots for numerical data"""
    n_vars = len(numerical_data)
    if n_vars == 0:
        print("No numerical data available for plotting.")
        return

    # Create subplots
    fig_size = (5 * min(n_vars, 2), 4 * ((n_vars + 1) // 2))
    fig, axes = plt.subplots(
        (n_vars + 1) // 2, min(n_vars, 2), figsize=fig_size, constrained_layout=True
    )

    # Handle single subplot case
    if n_vars == 1:
        axes = [axes] if not isinstance(axes, np.ndarray) else axes.flatten()
    elif isinstance(axes, np.ndarray):
        axes = axes.flatten()
    else:
        axes = [axes]

    for i, (var_name, data) in enumerate(numerical_data.items()):
        ax = axes[i]

        # Create histogram with density curve
        ax.hist(
            data, bins=20, alpha=0.7, density=True, color="skyblue", edgecolor="black"
        )

        # Add density curve
        data_range = np.linspace(data.min(), data.max(), 100)
        density = stats.gaussian_kde(data)
        ax.plot(data_range, density(data_range), "r-", linewidth=2, label="Density")

        # Add vertical lines for mean and median
        ax.axvline(
            data.mean(),
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Mean: {data.mean():.1f}",
        )
        ax.axvline(
            data.median(),
            color="green",
            linestyle="--",
            linewidth=2,
            label=f"Median: {data.median():.1f}",
        )

        # Formatting
        ax.set_title(
            f"Distribution of {var_name.title()}", fontsize=12, fontweight="bold"
        )
        ax.set_xlabel(var_name.replace("_", " ").title())
        ax.set_ylabel("Density")
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.savefig(f"{output_prefix}_distributions.png", dpi=150, bbox_inches="tight")
    plt.close()


def create_box_plots(numerical_data, output_prefix):
    """Create box plots for outlier detection"""
    n_vars = len(numerical_data)
    if n_vars == 0:
        return

    fig, axes = plt.subplots(
        1, n_vars, figsize=(4 * n_vars, 6), constrained_layout=True
    )

    if n_vars == 1:
        axes = [axes]

    for i, (var_name, data) in enumerate(numerical_data.items()):
        ax = axes[i]

        # Create box plot
        bp = ax.boxplot(
            data, patch_artist=True, boxprops=dict(facecolor="lightblue", alpha=0.7)
        )

        # Add mean marker
        ax.plot(
            [1], [data.mean()], "ro", markersize=8, label=f"Mean: {data.mean():.1f}"
        )

        ax.set_title(f"Box Plot: {var_name.title()}", fontsize=12, fontweight="bold")
        ax.set_ylabel(var_name.replace("_", " ").title())
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.savefig(f"{output_prefix}_boxplots.png", dpi=150, bbox_inches="tight")
    plt.close()


def main():
    # Get command line arguments
    if len(sys.argv) < 2:
        print(
            "Usage: python analyze_csv_descriptive_stats.py <csv_path> [output_prefix]"
        )
        sys.exit(1)

    csv_path = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else "descriptive_stats"

    # Load data
    try:
        df = pd.read_csv(csv_path)
        print(f"Data loaded successfully: {len(df)} rows, {len(df.columns)} columns\n")
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # Extract numerical data
    numerical_data = extract_numerical_data(df)

    if not numerical_data:
        print("No numerical data found in the dataset.")
        sys.exit(1)

    # Calculate descriptive statistics
    stats_list = []
    for var_name, data in numerical_data.items():
        stats = calculate_descriptive_stats(data, var_name)
        if stats:
            stats_list.append(stats)

    # Display results
    stats_table = format_stats_table(stats_list)
    print(stats_table)

    # Save results to file
    with open(f"{output_prefix}_report.txt", "w", encoding="utf-8") as f:
        f.write(stats_table)
        f.write("\n\nDetailed Analysis:\n")
        f.write("=" * 50 + "\n")

        for stats in stats_list:
            f.write(f"\n{stats['name'].upper()}:\n")
            f.write(f"  Sample size: {stats['count']}\n")
            f.write(
                f"  Central tendency: Mean={stats['mean']:.2f}, Median={stats['median']:.2f}\n"
            )
            f.write(f"  Spread: Std={stats['std']:.2f}, Range={stats['range']:.2f}\n")
            f.write(
                f"  Shape: Skewness={stats['skewness']:.3f}, Kurtosis={stats['kurtosis']:.3f}\n"
            )
            f.write(
                f"  Outliers: {stats['outlier_count']} ({stats['outlier_percentage']:.1f}%)\n"
            )

    # Create visualizations
    print(f"\nCreating distribution plots...")
    create_distribution_plots(numerical_data, output_prefix)

    print(f"Creating box plots...")
    create_box_plots(numerical_data, output_prefix)

    print(f"\nAnalysis complete!")
    print(f"Report saved to: {output_prefix}_report.txt")
    print(f"Distribution plots saved to: {output_prefix}_distributions.png")
    print(f"Box plots saved to: {output_prefix}_boxplots.png")


if __name__ == "__main__":
    # Import scipy.stats for density estimation
    from scipy import stats

    main()
