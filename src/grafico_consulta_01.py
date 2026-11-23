import matplotlib.pyplot as plt
from pathlib import Path

# Resultados obtenidos mediante PySpark
rangos = ["Menos de 30", "30-39", "40-49", "50-59", "60 o más"]

mujeres = [10.62, 8.71, 6.67, 5.10, 4.51]
hombres = [12.52, 10.97, 9.42, 8.81, 6.39]

x = range(len(rangos))
ancho = 0.35

fig, ax = plt.subplots(figsize=(11, 6))

barras_m = ax.bar(
    [i - ancho / 2 for i in x],
    mujeres,
    ancho,
    label="Mujeres",
    color="#E69F00"
)

barras_h = ax.bar(
    [i + ancho / 2 for i in x],
    hombres,
    ancho,
    label="Hombres",
    color="#0072B2"
)

ax.set_title("Tasa de impago por edad y género - Home Credit")
ax.set_xlabel("Rango de edad")
ax.set_ylabel("Tasa de impago (%)")
ax.set_xticks(list(x))
ax.set_xticklabels(rangos)
ax.legend()
ax.grid(axis="y", alpha=0.25)

ax.bar_label(barras_m, fmt="%.2f%%", padding=3)
ax.bar_label(barras_h, fmt="%.2f%%", padding=3)

ax.set_ylim(0, 15)

fig.tight_layout()

# Guardar la imagen en la carpeta resultados
salida = Path("resultados/grafico_consulta_01.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
