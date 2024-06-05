from matplotlib import pyplot as plt

x = []
czebyszew = []
dokladne = []
rownoodlegle = []

with open("results_czebyszew.txt") as f:
    for line in f:
        data = line.split()
        x.append(float(data[0]))
        czebyszew.append(float(data[1]))

with open("results_dokladne.txt") as f:
    for line in f:
        data = line.split()
        dokladne.append(float(data[1]))

with open("results_rownoodlegle.txt") as f:
    for line in f:
        data = line.split()
        rownoodlegle.append(float(data[1]))

plt.plot(x, dokladne, label="Rozwiązanie dokładne")
plt.plot(x, czebyszew, label="Rozwiązania Czebyszew", linestyle='none', marker='.', markersize=3)
plt.plot(x, rownoodlegle, label="Rozwiązania rownoodległe", linestyle='none', marker='.', markersize=3)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.title("Wykres interpolacji na węzłach równoodległych oraz węzłach Czebyszewa, wraz z dokładnym wykresem funkcji analitycznej")

plt.show()