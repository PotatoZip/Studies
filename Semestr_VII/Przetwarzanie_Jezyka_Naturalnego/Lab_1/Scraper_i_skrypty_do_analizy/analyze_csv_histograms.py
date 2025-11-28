import sys
import pandas as pd
import matplotlib.pyplot as plt

csv_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv) > 2 else "multi_histograms.png"

df = pd.read_csv(csv_path)


def plot_counts(ax, series, title, bar_width=0.6):
    s = series.astype(str).str.strip()
    s = s[s != ""]
    counts = s.value_counts()

    positions = range(len(counts))
    ax.bar(positions, counts.values, width=bar_width)
    ax.set_xticks(positions)
    ax.set_xticklabels(counts.index, rotation=45, ha="right")

    ax.set_title(title)
    ax.set_ylabel("Liczba")


fig, axes = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)

plot_counts(axes[0], df["spec_marka_procesora"], "Marka procesora", bar_width=0.55)
plot_counts(axes[1], df["spec_system_operacyjny"], "System operacyjny", bar_width=0.55)
plot_counts(axes[2], df["spec_typ_produktu"], "Typ produktu", bar_width=0.55)

plt.savefig(out_path, dpi=150)
