from matplotlib import pyplot as plt


x = []
roz_analit = []
euler_b = []
euler_p = []
trapez = []

with open("stable.txt") as f:
    for line in f:
        data = line.split()
        x.append(float(data[0]))
        roz_analit.append(float(data[1]))
        euler_b.append(float(data[2]))
        euler_p.append(float(data[3]))
        trapez.append(float(data[4]))

plt.plot(x, roz_analit, label="Rozwiazanie analityczne")
plt.plot(x, euler_b, label="Euler bezposredni", linestyle='none', marker='.', markersize=3)
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("Porównanie metody Bezośredniej Eulera z rozwiązaniem analitycznym")
plt.show()

plt.plot(x, roz_analit, label="Rozwiazanie analityczne")
plt.plot(x, euler_p, label="Euler pośredni", linestyle='none', marker='.', markersize=3)
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("Porównanie metody Pośredniej Eulera z rozwiązaniem analitycznym")
plt.show()

plt.plot(x, roz_analit, label="Rozwiazanie analityczne")
plt.plot(x, trapez, label="Metoda trapezów", linestyle='none', marker='.', markersize=3)
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("Porównanie metody trapezów z rozwiązaniem analitycznym")
plt.show()

x = []
roz_analit = []
euler_b = []

with open("unstable.txt") as f:
    for line in f:
        data = line.split()
        x.append(float(data[0]))
        roz_analit.append(float(data[1]))
        euler_b.append(float(data[2]))
        
plt.plot(x, roz_analit, label="Rozwiazanie analityczne")
plt.plot(x, euler_b, label="Euler bezposredni", linestyle='none', marker='.', markersize=3)
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("Porównanie metody Bezośredniej Eulera (niestabilnej) z rozwiązaniem analitycznym")
plt.show()

x = []
err_bme = []
err_pme = []
err_pmt = []

with open("BME_err.txt") as f:
    for line in f:
        data = line.split()
        x.append(float(data[0]))
        err_bme.append(float(data[1]))

with open("PME_err.txt") as f:
    for line in f:
        data = line.split()
        err_pme.append(float(data[1]))
with open("PMT_err.txt") as f:
    for line in f:
        data = line.split()
        err_pmt.append(float(data[1]))


print(err_bme)
plt.plot(x, err_bme, label="Euler bezposredni", linestyle='none', marker='.', markersize=3)
plt.plot(x, err_pme, label="Euler pośredni", linestyle='none', marker='.', markersize=3)
plt.plot(x, err_pmt, label="Metoda trapezów", linestyle='none', marker='.', markersize=3)
plt.xlabel("log10(h)")
plt.ylabel("log10(Blad)")
plt.legend()
plt.title("Rząd wielkości wartości błędu bezwzględnego dla podanych metod")
plt.show()