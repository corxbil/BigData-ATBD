import matplotlib.pyplot as plt
from pathlib import Path

# Resultados obtenidos con PySpark en la consulta 3
niveles = [
    "Sin retrasos",
    "1-7 días",
    "8-30 días",
    "31-90 días",
    "Más de 90 días"
]

tasas = [6.80, 8.80, 9.75, 11.32, 9.63]

fig, ax = plt.subplots(figsize=(11, 6))

barras = ax.bar(
    niveles,
    tasas,
    color="#277DA1"
)

ax.set_title("Consulta 03 - Tasa de impago según retrasos en los pagos")
ax.set_xlabel("Máximo retraso histórico registrado")
ax.set_ylabel("Tasa de impago (%)")

ax.set_ylim(0, 13)
ax.grid(axis="y", alpha=0.25)

ax.bar_label(barras, fmt="%.2f%%", padding=3)

fig.tight_layout()

# Guardar el gráfico
salida = Path("resultados/grafico_consulta_03.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
