from pathlib import Path
import sys

import numpy as np
import pandas as pd


# -------------------------------------------------
# Generator danych do zaliczenia z analiz
# nieparametrycznych: Kruskal-Wallis, Friedman,
# Scheirer-Ray-Hare, Cochran Q.
#
# Ważne:
# - brak stałego ziarna losowania,
# - przy każdym uruchomieniu dane są inne,
# - można opcjonalnie podać identyfikator studenta,
#   który zostanie dopisany do nazwy pliku.
#
# Uruchomienie:
#   python generuj_losowe_dane_zaliczenie_nieparametryczne_anova.py
#   python generuj_losowe_dane_zaliczenie_nieparametryczne_anova.py 12345
# -------------------------------------------------

rng = np.random.default_rng()

student_tag = sys.argv[1].strip() if len(sys.argv) > 1 else ""
filename = "dane_zaliczenie_nieparametryczne_anova"
if student_tag:
    filename += f"_{student_tag}"
filename += ".xlsx"

output_path = Path.cwd() / filename


# =============================
# 1. Kruskal-Wallis
# =============================
n_per_group = 18

times_A = rng.lognormal(mean=4.20, sigma=0.22, size=n_per_group)
times_B = rng.lognormal(mean=4.45, sigma=0.23, size=n_per_group)
times_C = rng.lognormal(mean=4.65, sigma=0.25, size=n_per_group)

kruskal = pd.DataFrame({
    "metoda": np.repeat(["A", "B", "C"], n_per_group),
    "czas_s": np.round(np.concatenate([times_A, times_B, times_C]), 2)
})


# =============================
# 2. Friedman
# =============================
n_students = 18
baseline = rng.normal(78, 7, n_students)

ide_A = baseline + rng.normal(0, 3, n_students)
ide_B = baseline - 5 + rng.normal(0, 3, n_students)
ide_C = baseline - 9 + rng.normal(0, 3, n_students)

friedman = pd.DataFrame({
    "student_id": np.arange(1, n_students + 1),
    "IDE_A": np.round(ide_A, 2),
    "IDE_B": np.round(ide_B, 2),
    "IDE_C": np.round(ide_C, 2)
})


# =============================
# 3. Scheirer-Ray-Hare
# =============================
rows = []
for storage in ["HDD", "SATA_SSD", "NVMe"]:
    for load in ["Niskie", "Średnie", "Wysokie"]:
        for _ in range(12):
            mu = 4.55

            if storage == "SATA_SSD":
                mu -= 0.12
            elif storage == "NVMe":
                mu -= 0.28

            if load == "Średnie":
                mu += 0.12
            elif load == "Wysokie":
                mu += 0.30

            if storage == "NVMe" and load == "Wysokie":
                mu += 0.10
            if storage == "HDD" and load == "Wysokie":
                mu += 0.15

            latency = rng.lognormal(mean=mu, sigma=0.24)
            rows.append((storage, load, round(float(latency), 2)))

scheirer_ray_hare = pd.DataFrame(rows, columns=["storage", "load", "latency_ms"])


# =============================
# 4. Cochran Q
# =============================
n_cases = 20
alg_A = rng.binomial(1, 0.55, n_cases)
alg_B = rng.binomial(1, 0.75, n_cases)
alg_C = rng.binomial(1, 0.85, n_cases)

cochran_q = pd.DataFrame({
    "alg_A": alg_A,
    "alg_B": alg_B,
    "alg_C": alg_C
})


# =============================
# Zapis do Excela
# =============================
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    kruskal.to_excel(writer, sheet_name="kruskal", index=False)
    friedman.to_excel(writer, sheet_name="friedman", index=False)
    scheirer_ray_hare.to_excel(writer, sheet_name="scheirer_ray_hare", index=False)
    cochran_q.to_excel(writer, sheet_name="cochran_q", index=False)

print(f"Gotowe. Utworzono plik: {output_path}")
print("Przy każdym uruchomieniu dane będą inne, ponieważ generator nie ma ustawionego stałego ziarna.")
