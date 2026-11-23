import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

ocupaciones = [
    "Accountants",
    "Cleaning staff",
    "Cooking staff",
    "Core staff",
    "Drivers",
    "HR staff",
    "High skill tech staff",
    "IT staff",
    "Laborers",
    "Low-skill Laborers",
    "Managers",
    "Medicine staff",
    "Private service staff",
    "Realty agents",
    "Sales staff",
    "Secretaries",
    "Security staff",
    "Waiters/barmen staff"
]

antiguedad = [
    "Menos de 2",
    "2-4",
    "5-9",
    "10-19",
    "20 o más"
]

# Filas: ocupaciones
# Columnas: rangos de antigüedad
tasas = np.array([
    [5.98, 5.19, 4.77, 2.93, 4.03],
    [10.33, 12.13, 8.52, 4.65, 7.33],
    [12.92, 11.45, 9.27, 6.94, 4.30],
    [8.03, 8.16, 5.24, 4.23, 3.49],
    [13.64, 12.91, 8.72, 7.65, 6.44],
    [9.79, 5.23, 6.52, 2.35, 8.00],
    [8.06, 6.92, 5.82, 3.91, 3.99],
    [9.93, 8.38, 2.27, 1.89, 4.35],
    [13.66, 12.31, 9.06, 7.05, 4.63],
    [20.89, 17.57, 14.89, 9.42, 0.00],
    [9.20, 7.16, 5.78, 3.76, 3.42],
    [9.53, 8.25, 6.62, 5.76, 3.55],
    [8.53, 8.72, 4.02, 4.36, 6.49],
    [8.99, 8.68, 6.93, 4.55, 0.00],
    [11.22, 10.56, 8.06, 5.64, 6.12],
    [9.18, 6.98, 5.85, 8.02, 2.27],
    [12.18, 11.63, 9.25, 7.98, 9.29],
    [15.09, 12.11, 7.74, 8.51, 0.00]
])

fig, ax = plt.subplots(figsize=(13, 11))

imagen = ax.imshow(
    tasas,
    cmap="YlOrRd",
    aspect="auto",
    vmin=0,
    vmax=22
)

# Etiquetas
ax.set_xticks(np.arange(len(antiguedad)))
ax.set_xticklabels(antiguedad)

ax.set_yticks(np.arange(len(ocupaciones)))
ax.set_yticklabels(ocupaciones)

ax.set_xlabel("Antigüedad laboral (años)")
ax.set_ylabel("Tipo de ocupación")
ax.set_title(
    "Consulta 08 - Tasa de impago por ocupación y antigüedad laboral",
    pad=20
)

# Mostrar porcentajes dentro de las celdas
for i in range(len(ocupaciones)):
    for j in range(len(antiguedad)):
        valor = tasas[i, j]

        color_texto = "white" if valor >= 12 else "black"

        ax.text(
            j, i,
            f"{valor:.2f}%",
            ha="center",
            va="center",
            fontsize=8,
            color=color_texto
        )

# Escala de colores
barra_color = fig.colorbar(imagen, ax=ax)
barra_color.set_label("Tasa de impago (%)")

fig.tight_layout()

salida = Path("resultados/grafico_consulta_08.png")
salida.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(salida, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfico guardado en: {salida.resolve()}")
