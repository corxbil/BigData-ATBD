import matplotlib.pyplot as plt
from pathlib import Path

# Resultados reales obtenidos con PySpark
meses = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1]

utilizacion = [
    26.60, 27.00, 27.17, 27.55,
    28.16, 28.98, 30.20, 31.32,
    31.94, 33.44, 36.35, 42.97
]

fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(
    meses,
    utilizacion,
    marker="o",
    linewidth=2.5,
    markersize=7,
    color="#277DA1"
)

# Mostrar el porcentaje encima de cada punto
for mes, porcentaje in zip(meses, utilizacion):
    ax.annotate(
        f"{porcentaje:.2f}%",
        (mes, porcentaje),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=9
    )

ax.set_title(
    "Consulta 07 - Evolución mensual de utilización de tarjetas de crédito"
)
ax.set_xlabel("Mes relativo (MONTHS_BALANCE)")
ax.set_ylabel("Utilización media del límite de crédito (%)")

ax.set_xticks(meses)
ax.set_ylim(0, 50)
ax.grid(alpha=0.25)

fig.tight_layout()

salida = Path("resultados/grafico_consulta_07.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
