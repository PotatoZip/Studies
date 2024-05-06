import matplotlib.pyplot as plt
import numpy

log10h,progresywna_srodek,wsteczna_srodek,centralna_srodek = [],[],[],[]
progresywna_poczatek,wsteczna_koniec = [],[]
progresywna3_poczatek,wsteczna3_koniec = [],[]
with open('wynikfloat.txt') as f:
    for i, line in enumerate(f):
        index = i % 8
        value = float(line.strip())  
        if index == 0:
            log10h.append(value)
        elif index == 1:
            progresywna_srodek.append(value)
        elif index == 2:
            wsteczna_srodek.append(value)
        elif index == 3:
            centralna_srodek.append(value)
        elif index == 4:
            progresywna_poczatek.append(value)
        elif index == 5:
            wsteczna_koniec.append(value)
        elif index == 6:
            progresywna3_poczatek.append(value)
        elif index == 7:
            wsteczna3_koniec.append(value)



plt.figure(figsize=(16, 16))


plt.plot(log10h, progresywna_srodek, label='progresywna srodkowa', linestyle='', marker='o', markersize=5)
plt.plot(log10h, wsteczna_srodek, label='wsteczna srodkowa', linestyle='', marker='o', markersize=5)
plt.plot(log10h, centralna_srodek, label='centralna srodkowa', linestyle='', marker='o', markersize=5)

plt.plot(log10h, progresywna_poczatek, label='progresywna poczatkowa', linestyle='', marker='o', markersize=5)
plt.plot(log10h, wsteczna_koniec, label='wsteczna koncowa', linestyle='', marker='o', markersize=5)

plt.plot(log10h, progresywna3_poczatek, label='progresywna poczatkowa 3', linestyle='', marker='o', markersize=5)
plt.plot(log10h, wsteczna3_koniec, label='wsteczna koncowa 3', linestyle='', marker='o', markersize=5)

plt.title('Wykres Double')

plt.xlabel('log10(h)')
plt.ylabel('log10(blad)')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()
