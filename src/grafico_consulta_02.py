import matplotlib.pyplot as plt
from pathlib import Path

niveles = [
    "Sin deuda\nregistrada",
    "Menos de\n100.000",
    "100.000-\n499.999",
    "500.000-\n999.999",
    "1.000.000\no más"
]

tasas = [7.28, 7.89, 8.41, 9.21, 9.01]

fig, ax = plt.subplots(figsize=(11, 6))

barras = ax.bar(niveles, tasas)

ax.set_title("Consulta 02 - Tasa de impago por nivel de deuda externa")
ax.set_xlabel("Nivel de deuda")
ax.set_ylabel("Tasa de impago (%)")
ax.grid(axis="y", alpha=0.25)
ax.set_ylim(0, 11)

ax.bar_label(barras, fmt="%.2f%%", padding=3)

fig.tight_layout()

salida = Path("resultados/grafico_consulta_02.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")