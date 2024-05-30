import numpy as np
import matplotlib.pyplot as plt

# Funkcja do wczytania danych dla osi X
def load_x_data(filename):
    with open(filename, 'r') as file:
        x_data = np.loadtxt(file)
    return x_data

# Funkcja do wczytania danych dla osi Y
def load_y_data(filename):
    y_data = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split(';')
            row_float = []
            for value in row:
                try:
                    row_float.append(float(value))
                except ValueError:
                    pass  # Ignorowanie pustych wartości lub niemożliwych do przekonwertowania
            if row_float:
                y_data.append(row_float)
    return np.array(y_data)

# Wczytaj dane
x_filename = 'os_x_laasonen.txt'
y_filename = 'analityczne.txt'
y2_filename = 'laasonen_thomas.txt'

x_data = load_x_data(x_filename)
y_data = load_y_data(y_filename)
y2_data = load_y_data(y2_filename)

# Sprawdzenie, czy liczba punktów w osi X zgadza się z liczbą kolumn w macierzy Y
if x_data.shape[0] != y_data.shape[1]:
    raise ValueError("Liczba punktów w osi X musi odpowiadać liczbie kolumn w macierzy Y.")

# Obliczenie średniej dla każdej kolumny danych
y_mean = np.mean(y_data, axis=0)
y2_mean = np.mean(y2_data, axis=0)

# Rysowanie wykresu
plt.figure(figsize=(10, 6))

plt.plot(x_data, y_mean, label='Wartość Dokładna')
plt.plot(x_data, y2_mean, 'o--', label='Wartość Obliczona')
plt.xlabel('Oś X')
plt.ylabel('Oś Y')
plt.title('Wykres rozwiązań numerycznych i analitycznych dla wartości czasu t = 0.5')
plt.grid(True)
plt.legend()
plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt

# # Wczytanie danych z plików TXT
# x_data1 = pd.read_csv('os_x_laasonen.txt', sep='\t', header=None)  # Zmień sep='\t' na odpowiedni separator (np. ' ', ',' itp.)
# y_data1 = pd.read_csv('analityczne.txt', sep='\t', header=None)  # Zmień sep='\t' na odpowiedni separator (np. ' ', ',' itp.)
# x_data2 = pd.read_csv('os_x_laasonen.txt', sep='\t', header=None)  # Plik z danymi dla drugiego wykresu
# y_data2 = pd.read_csv('laasonen_thomas.txt', sep='\t', header=None)  # Plik z danymi dla drugiego wykresu

# # Zakładamy, że dane są w jednej kolumnie, bez nagłówków
# x_values1 = x_data1.iloc[:, 0].values
# y_values1 = y_data1.iloc[:, 0].values
# x_values2 = x_data2.iloc[:, 0].values
# y_values2 = y_data2.iloc[:, 0].values

# # Tworzenie wykresu
# plt.figure(figsize=(10, 6))

# # Pierwszy wykres - ciągła linia
# plt.plot(x_values1, y_values1, marker='', linestyle='-', color='b', label='Błąd 1')

# # Drugi wykres - kropkowana linia
# plt.plot(x_values2, y_values2, marker='o', linestyle=':', color='r', label='Błąd 2')

# # Dodanie tytułu i etykiet osi
# plt.title('Maksymalny błąd od czasu (Metoda KMB)')
# plt.xlabel('T')
# plt.ylabel('|Maksymalny Błąd X|')

# # Dodanie legendy
# plt.legend()

# # Wyświetlenie wykresu
# plt.show()
