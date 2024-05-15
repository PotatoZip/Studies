import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    x_values = []
    y_values = []
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split()
            if len(data) == 2:
                x_values.append(float(data[0]))
                y_values.append(float(data[1]))
    return x_values, y_values

try:
    x_analityczne, y_analityczne = read_data('analitic_solution.txt')
    x_numerow, y_numerow = read_data('numerow.txt')
    x_trzypunktowe, y_trzypunktowe = read_data('three_point.txt')


    
    plt.figure(figsize=(10, 6))
    plt.plot(x_analityczne, y_analityczne, label='Analityczne', color='red', linestyle='solid')
    plt.plot(x_numerow, y_numerow, label='Numerow', color='blue', linestyle='dotted')
    plt.plot(x_trzypunktowe, y_trzypunktowe, label='Trzy punktowa', color='green', linestyle='dotted')

    plt.title('Wykres danych')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

except FileNotFoundError:
    print('Brak pliku z danymi')