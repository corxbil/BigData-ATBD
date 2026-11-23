import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Resultados reales de PySpark - Consulta 04
educacion = [
    "Academic degree",
    "Higher education",
    "Incomplete higher",
    "Lower secondary",
    "Secondary / secondary special"
]

menos_100k = [0.00, 5.96, 9.28, 9.29, 8.49]
de_100_200k = [0.00, 5.69, 8.74, 12.57, 9.33]
de_200_300k = [2.08, 5.26, 7.76, 10.50, 8.72]
mas_300k = [4.88, 4.12, 7.78, 5.62, 7.84]

x = np.arange(len(educacion))
ancho = 0.2

fig, ax = plt.subplots(figsize=(14, 7))

ax.bar(x - 1.5 * ancho, menos_100k, ancho, label="< 100.000")
ax.bar(x - 0.5 * ancho, de_100_200k, ancho, label="100.000-199.999")
ax.bar(x + 0.5 * ancho, de_200_300k, ancho, label="200.000-299.999")
ax.bar(x + 1.5 * ancho, mas_300k, ancho, label="300.000 o más")

ax.set_title("Consulta 04 - Tasa de impago por educación e ingresos")
ax.set_xlabel("Nivel educativo")
ax.set_ylabel("Tasa de impago (%)")

ax.set_xticks(x)
ax.set_xticklabels(
    [
        "Academic\ndegree",
        "Higher\neducation",
        "Incomplete\nhigher",
        "Lower\nsecondary",
        "Secondary /\nsecondary special"
    ]
)

ax.legend(title="Rango de ingresos")
ax.grid(axis="y", alpha=0.25)
ax.set_ylim(0, 15)

fig.tight_layout()

salida = Path("resultados/grafico_consulta_04.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
