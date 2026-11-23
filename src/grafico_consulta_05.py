import matplotlib.pyplot as plt
from pathlib import Path

# Resultados obtenidos con PySpark - Consulta 05
grupos = ["0", "1", "2-3", "4-6", "7 o más"]
tasas = [5.96, 8.38, 7.84, 7.77, 8.96]

fig, ax = plt.subplots(figsize=(11, 6))

barras = ax.bar(
    grupos,
    tasas,
    color="#277DA1"
)

ax.set_title("Consulta 05 - Tasa de impago según solicitudes previas")
ax.set_xlabel("Número de solicitudes de crédito previas")
ax.set_ylabel("Tasa de impago (%)")

ax.set_ylim(0, 11)
ax.grid(axis="y", alpha=0.25)

ax.bar_label(barras, fmt="%.2f%%", padding=3)

fig.tight_layout()

# Guardar el gráfico
salida = Path("resultados/grafico_consulta_05.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
