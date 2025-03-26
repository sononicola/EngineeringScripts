import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid  

# Dati di input
x = np.array([-1, -0.5, 0.5, 1, 2])
y = np.array([1, 1, 1, -0.5, -1])
x = np.linspace(-50,50,1000)
y=x**2-500
plt.plot(x,y)
plt.show()
# Trova gli indici dove y cambia segno
zero_crossings = np.where(np.diff(np.sign(y)))[0]

# Calcola i punti di intersezione con l'asse x
x_intersections = []
for index in zero_crossings:
    # Interpolazione lineare per trovare il punto in cui y = 0
    x0, x1 = x[index], x[index + 1]
    y0, y1 = y[index], y[index + 1]

    # Calcola il punto di intersezione
    x_intersect = x0 - (y0 * (x1 - x0)) / (y1 - y0)
    x_intersections.append(x_intersect)

# Converti in array NumPy
x_intersections = np.array(x_intersections)
# Unisci i vettori originali con i punti di intersezione
x_combined = np.concatenate((x, x_intersections))
y_combined = np.concatenate((y, np.zeros_like(x_intersections)))
print(x_intersections)
# Ordina i vettori risultanti
sorted_indices = np.argsort(x_combined)
print(sorted_indices)
x_sorted = x_combined[sorted_indices]
y_sorted = y_combined[sorted_indices]

print(x_sorted)
zero_crossings = np.where(np.isin(x_sorted, x_intersections))[0]

print(zero_crossings)
# Aggiungi gli estremi
zero_crossings = np.concatenate(([0], zero_crossings, [len(x_sorted) - 1]))
print(zero_crossings)

# Calcola l'area tra i punti
areas = []
for i in range(len(zero_crossings) - 1):
    start = zero_crossings[i]
    end = zero_crossings[i + 1]
    area = trapezoid(y_sorted[start : end + 1], x_sorted[start : end + 1])
    areas.append(area)

# Plot dei dati
plt.figure(figsize=(10, 6))
plt.plot(x_sorted, y_sorted, color="blue", marker="o")

# Riempie le aree sotto la curva con colori diversi
for i in range(len(areas)):
    start = zero_crossings[i]
    end = zero_crossings[i + 1]
    color = (
        "blue" if areas[i] >= 0 else "red"
    )  # Colore blu se l'area è positiva, rosso se negativa
    plt.fill_between(
        x_sorted[start : end + 1],
        y_sorted[start : end + 1],
        color=color,
        alpha=0.5,
        label=f"Area {i + 1}: {areas[i]:.2f}",
    )

    # Aggiungi il testo dell'area al centro di ogni tratto
    mid_x = (x_sorted[start] + x_sorted[end]) / 2
    mid_y = (y_sorted[start] + y_sorted[end]) / 2
    plt.text(
        mid_x,
        mid_y,
        f"{areas[i]:.2f}",
        ha="center",
        va="center",
        fontsize=10,
        color="black",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )
# Aggiungi linee verticali per le intersezioni
for x_intersect in x_intersections:
    plt.axvline(x=x_intersect, color="red", linestyle="--")
    plt.text(
        x_intersect,
        0.1,
        f"x = {x_intersect:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
        color="black",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )
# Aggiungi etichette e titolo
plt.title("Intersezioni con l'asse x e aree sottostanti")
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0, color="black", lw=0.5, ls="--")  
plt.axvline(0, color="black", lw=0.5, ls="--")  
plt.legend()
plt.grid()
plt.show()

# Stampa le aree calcolate
for i, area in enumerate(areas):
    print(f"Area tra l'intersezione {i + 1} e {i + 2}: {area:.2f}")
