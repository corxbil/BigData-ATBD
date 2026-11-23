import matplotlib.pyplot as plt
from pathlib import Path

# Resultados de PySpark - Consulta 10
grupos = ["0", "1", "2-3", "4-6", "7 o más"]
tasas = [7.00, 7.74, 8.76, 10.45, 12.23]

fig, ax = plt.subplots(figsize=(11, 6))

barras = ax.bar(
    grupos,
    tasas,
    color="#277DA1"
)

ax.set_title(
    "Consulta 10 - Tasa de impago según solicitudes rechazadas o canceladas"
)
ax.set_xlabel("Número de solicitudes anteriores rechazadas o canceladas")
ax.set_ylabel("Tasa de impago (%)")

ax.set_ylim(0, 15)
ax.grid(axis="y", alpha=0.25)

ax.bar_label(barras, fmt="%.2f%%", padding=3)

fig.tight_layout()

# Guardar la gráfica
salida = Path("resultados/grafico_consulta_10.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
