from pathlib import Path
import re
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_BREAK

base = Path.cwd()
origen = base / "documentacion" / "informe_final_completo.md"
destino = base / "documentacion" / "informe_final.docx"

if destino.exists():
    raise FileExistsError(f"Ya existe: {destino}")

texto = origen.read_text(encoding="utf-8-sig")
documento = Document()

seccion = documento.sections[0]
seccion.top_margin = Cm(2.3)
seccion.bottom_margin = Cm(2.3)
seccion.left_margin = Cm(2.5)
seccion.right_margin = Cm(2.5)

normal = documento.styles["Normal"]
normal.font.name = "Aptos"
normal.font.size = Pt(10.5)
normal.paragraph_format.space_after = Pt(6)

imagenes = 0
titulos = 0

for linea in texto.splitlines():
    linea = linea.strip()

    if not linea:
        continue

    imagen = re.fullmatch(r'!\[(.*?)\]\((.*?)\)', linea)
    if imagen:
        ruta = (origen.parent / imagen.group(2)).resolve()

        if not ruta.is_file():
            raise FileNotFoundError(f"Falta la imagen: {ruta}")

        parrafo = documento.add_paragraph()
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        parrafo.add_run().add_picture(str(ruta), width=Cm(15.5))
        imagenes += 1
        continue

    titulo = re.match(r'^(#{1,3})\s+(.+)$', linea)
    if titulo:
        nivel = len(titulo.group(1))
        documento.add_heading(titulo.group(2), level=nivel)
        titulos += 1
        continue

    if linea.startswith("- "):
        documento.add_paragraph(linea[2:], style="List Bullet")
        continue

    if linea.startswith("<!--"):
        continue

    if linea.startswith("|"):
        documento.add_paragraph(linea)
        continue

    if linea == "---":
        continue

    documento.add_paragraph(linea)

documento.save(destino)

print("DOCUMENTO WORD GENERADO CORRECTAMENTE")
print(f"Archivo: {destino}")
print(f"Titulos incorporados: {titulos}")
print(f"Graficas incorporadas: {imagenes}")

if imagenes != 10:
    raise RuntimeError(f"Se esperaban 10 graficas, se encontraron {imagenes}")
