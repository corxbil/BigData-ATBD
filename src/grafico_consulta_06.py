import matplotlib.pyplot as plt
from pathlib import Path

# Resultados obtenidos con PySpark - Consulta 06
niveles = [
    "Menos del 20%",
    "20%-39%",
    "40%-59%",
    "60%-79%",
    "80% o más"
]

tasas = [7.62, 7.93, 8.27, 8.15, 9.55]

fig, ax = plt.subplots(figsize=(11, 6))

barras = ax.bar(
    niveles,
    tasas,
    color="#277DA1"
)

ax.set_title(
    "Consulta 06 - Tasa de impago según carga financiera familiar"
)
ax.set_xlabel("Nivel de carga financiera familiar")
ax.set_ylabel("Tasa de impago (%)")

ax.set_ylim(0, 12)
ax.grid(axis="y", alpha=0.25)

ax.bar_label(barras, fmt="%.2f%%", padding=3)

fig.tight_layout()

# Guardar el gráfico en la carpeta resultados
salida = Path("resultados/grafico_consulta_06.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
