import sys
import pandas as pd
import matplotlib.pyplot as plt
import re

csv_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv) > 2 else "correlations_price.png"

df = pd.read_csv(csv_path)


def extract_number(value):
    if pd.isna(value) or value == 0:
        return None
    match = re.search(r"(\d+(?:[.,]\d+)?)", str(value))
    if match:
        return float(match.group(1).replace(",", "."))
    return None


def parse_storage_size(value):
    if pd.isna(value):
        return None
    text = str(value).strip().upper().replace(",", ".")
    match = re.search(r"(\d+(?:\.\d+)?)\s*([TGM]?B)?", text)
    if not match:
        return None
    num = float(match.group(1))
    unit = match.group(2) or "GB"

    if "TB" in unit:
        num *= 1024
    elif "MB" in unit:
        num /= 1024
    return num


df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["ram_gb"] = df["spec_pami_ram"].apply(extract_number)
df["disk_gb"] = df["spec_pojemno_dysku_1"].apply(parse_storage_size)
df["cores"] = pd.to_numeric(df["spec_liczba_rdzeni"], errors="coerce")

fig, axes = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)


def plot_corr(ax, x, y, xlabel, ylabel="Cena [PLN]"):
    ax.scatter(x, y, alpha=0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.5)


plot_corr(axes[0], df["ram_gb"], df["price"], "RAM [GB]")
plot_corr(axes[1], df["disk_gb"], df["price"], "Dysk [GB]")
plot_corr(axes[2], df["cores"], df["price"], "Liczba rdzeni")

plt.suptitle("Zależność ceny od parametrów technicznych", fontsize=13)
plt.savefig(out_path, dpi=150)
