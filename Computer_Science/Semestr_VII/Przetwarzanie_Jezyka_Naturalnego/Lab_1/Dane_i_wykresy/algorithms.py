import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay


# Wczytanie danych
df = pd.read_csv("mediamarkt_desktops_normalized.csv")


# Konwersja pojemności
def parse_gb(x):
    if pd.isna(x):
        return np.nan
    s = str(x).lower().replace(",", ".")
    if "tb" in s:
        return float(s.split()[0]) * 1024
    elif "gb" in s:
        return float(s.split()[0])
    try:
        return float(s)
    except:
        return np.nan


df["ram_gb"] = df["spec_pami_ram"].apply(parse_gb)
df["disk_gb"] = df["spec_pojemno_dysku_1"].apply(parse_gb)
df = df.dropna(subset=["price", "ram_gb", "disk_gb"])

# Cena vs RAM
X = df[["ram_gb"]]
y = df["price"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model_ram = LinearRegression()
model_ram.fit(X_train, y_train)
y_pred_ram = model_ram.predict(X_test)

rmse_ram = mean_squared_error(y_test, y_pred_ram) ** 0.5
r2_ram = r2_score(y_test, y_pred_ram)
print(
    f"[RAM] Średni błąd przewidywania (RMSE)={rmse_ram:.2f} | Procent zmiennośći ceny (R²)={r2_ram:.3f}"
)

# Cena vs dysk
X2 = df[["disk_gb"]]
y2 = df["price"]
X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y2, test_size=0.3, random_state=42
)

model_disk = LinearRegression()
model_disk.fit(X2_train, y2_train)
y_pred_disk = model_disk.predict(X2_test)

rmse_disk = mean_squared_error(y2_test, y_pred_disk) ** 0.5
r2_disk = r2_score(y2_test, y_pred_disk)
print(
    f"[DYSK] Średni błąd przewidywania (RMSE)={rmse_disk:.2f} | Procent zmiennośći ceny (R²)={r2_disk:.3f}"
)

# Wizualizacja Regresji
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(
    df["ram_gb"], df["price"], color="blue", alpha=0.6, label="Dane rzeczywiste"
)
plt.plot(
    df["ram_gb"],
    model_ram.predict(df[["ram_gb"]]),
    color="red",
    label="Regresja liniowa",
)
plt.xlabel("Pamięć RAM [GB]")
plt.ylabel("Cena [zł]")
plt.title("Zależność ceny od pamięci RAM")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.scatter(
    df["disk_gb"], df["price"], color="green", alpha=0.6, label="Dane rzeczywiste"
)
plt.plot(
    df["disk_gb"],
    model_disk.predict(df[["disk_gb"]]),
    color="red",
    label="Regresja liniowa",
)
plt.xlabel("Pojemność dysku [GB]")
plt.ylabel("Cena [zł]")
plt.title("Zależność ceny od pojemności dysku")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Klasyfikacja
median_price = df["price"].median()
df["is_expensive"] = (df["price"] >= median_price).astype(int)

Xc = df[["ram_gb", "disk_gb"]]
yc = df["is_expensive"]

Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    Xc, yc, test_size=0.3, random_state=42, stratify=yc
)

clf = LogisticRegression(max_iter=1000)
clf.fit(Xc_train, yc_train)
yc_pred = clf.predict(Xc_test)

# Wyniki klasyfikacji
acc = accuracy_score(yc_test, yc_pred)
cm = confusion_matrix(yc_test, yc_pred, labels=[0, 1])
print(f"Dokładność klasyfikacji (CLS)={acc:.3f}")
print("Macierz pomyłek (wiersze = prawda, kolumny = pred):\n", cm)

# Wykres macierzy pomyłek
fig, ax = plt.subplots(figsize=(4, 4))
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["tani", "drogi"]).plot(
    ax=ax, values_format="d", colorbar=False
)
ax.set_title("Macierz pomyłek")
plt.tight_layout()
plt.show()
