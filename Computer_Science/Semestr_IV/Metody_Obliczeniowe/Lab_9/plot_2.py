import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('errors.txt')

log10h = data[:, 0]

blad_numerowa = data[:, 1]

blad_3_punktowy = data[:, 2]

plt.figure(figsize=(10, 6))

plt.plot(log10h, blad_numerowa, label='Blad dyskretyzacji Numerowa', color='red', marker='o', linestyle='None')


plt.plot(log10h, blad_3_punktowy, label='Blad dyskretyzacji 3 punktowej', color='green', marker='o', linestyle='None')

plt.title('Wykres błędów')
plt.xlabel('log10|h|')
plt.ylabel('log10|błąd|')

plt.legend()

plt.grid(True)
plt.show()