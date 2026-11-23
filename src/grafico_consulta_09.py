import matplotlib.pyplot as plt
from pathlib import Path

# Resultados obtenidos con PySpark - Consulta 09
meses = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1]

porcentajes = [
    3.47, 3.55, 3.64, 3.62,
    3.68, 3.68, 3.53, 3.58,
    3.90, 3.94, 4.19, 4.56
]

fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(
    meses,
    porcentajes,
    marker="o",
    linewidth=2.5,
    markersize=7,
    color="#277DA1"
)

# Mostrar los porcentajes encima de cada punto
for mes, porcentaje in zip(meses, porcentajes):
    ax.annotate(
        f"{porcentaje:.2f}%",
        (mes, porcentaje),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=9
    )

ax.set_title(
    "Consulta 09 - Evolución mensual de retrasos crediticios"
)
ax.set_xlabel("Mes relativo (MONTHS_BALANCE)")
ax.set_ylabel("Registros con retraso (%)")

ax.set_xticks(meses)
ax.set_ylim(0, 5.5)
ax.grid(alpha=0.25)

fig.tight_layout()

# Guardar la gráfica
salida = Path("resultados/grafico_consulta_09.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
