import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

def crear_linea_tiempo_desarrollo(texto, imagen_fondo, guardar_pdf=False):
    # Cargar la imagen de fondo
    bg_image = mpimg.imread(imagen_fondo)

    # Procesar eventos
    lineas = [linea.strip() for linea in texto.split('\n') if linea.strip()]
    eventos = []
    for linea in lineas:
        try:
            fecha_str = linea[:10]
            descripcion = linea[11:].strip()
            fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
            eventos.append((fecha, descripcion))
        except ValueError as e:
            print(f"Error al procesar la línea: {linea}")

    # Cambiar el orden del evento 5 (índice 4) para que esté después del 4 y comience un zigzag
    if len(eventos) > 4:
        evento_5 = eventos.pop(4)  # Extraer evento 5
        eventos.insert(4, evento_5)  # Insertarlo justo después del evento 4

    # Posiciones de los eventos
    n_eventos = len(eventos)
    x_positions = []
    y_positions = []

    for i in range(n_eventos):
        if i < 4:  # Los primeros 4 eventos se organizan de izquierda a derecha
            x = i * 3
            y = 0
        else:  # Después del evento 4, los eventos se organizan en zigzag
            fila = (i - 4) // 4  # Fila después del 4to evento
            pos_en_fila = (i - 4) % 4

            if fila % 2 == 0:  # Filas pares van de derecha a izquierda
                x = 9 - pos_en_fila * 3
            else:  # Filas impares van de izquierda a derecha
                x = pos_en_fila * 3

            y = -2 - fila * 2.2  # Desplazamiento vertical

        x_positions.append(x)
        y_positions.append(y)

    # Configurar el lienzo
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(15, 8))

    # Ajustar los límites en función de las posiciones de los eventos
    margin = 1.5
    ax.set_xlim(min(x_positions) - margin, max(x_positions) + margin)
    ax.set_ylim(min(y_positions) - margin, margin)

    # Redimensionar la imagen de fondo para cubrir el área de la línea de tiempo
    ax.imshow(bg_image, aspect='auto', extent=(min(x_positions) - margin, max(x_positions) + margin, min(y_positions) - margin, margin), alpha=0.9)

    # Dibujar conectores curvos y círculos decorativos
    for i in range(n_eventos - 1):
        x1, y1 = x_positions[i], y_positions[i]
        x2, y2 = x_positions[i + 1], y_positions[i + 1]

        # Crear conector en forma de "U"
        control1 = (x1, (y1 + y2) / 2)  # Punto de control 1, vertical desde el primer punto
        control2 = (x2, (y1 + y2) / 2)  # Punto de control 2, vertical desde el segundo punto

        verts = [
            (x1 , y1),  # Inicio
            control1,         # Punto de control 1
            control2,         # Punto de control 2
            (x2 , y2)    # Fin
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor='none', edgecolor='black', linewidth=2)
        ax.add_patch(patch)

    # Dibujar cajas y texto
    for i, ((fecha, desc), x, y) in enumerate(zip(eventos, x_positions, y_positions)):
        # Caja redondeada
        # Determinar el número de líneas en el texto para ajustar la altura de la caja
        texto_dividido = wrap_text(desc, 20)
        n_lineas = len(texto_dividido)
        altura_caja = 0.3 + n_lineas * 0.2  # Altura base + incremento por línea

        # Caja redondeada con altura ajustada
        rect = patches.FancyBboxPatch(
            (x - 0.7, y - altura_caja / 2),  # Centrar la caja verticalmente
            1.5, altura_caja,
            boxstyle=patches.BoxStyle("Round", pad=0.2),
            facecolor='white',
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(rect)

        # Círculo con número
        circle_y = y + altura_caja / 2 + 0.2
        circle = patches.Circle((x - 0.8, circle_y), 0.2, 
                                facecolor='#252440', 
                                edgecolor='black', 
                                linewidth=2)
        ax.add_patch(circle)
        ax.text(x - 0.8, circle_y, str(i + 1), 
                ha='center', va='center', 
                fontsize=12,  # Tamaño de letra
                color='white',
                fontweight='bold')

        # Texto del evento
        fecha_y = y + altura_caja / 2 + 0.02  # Ajustar posición de la fecha
        ax.text(x, fecha_y, fecha.strftime('%d/%m/%Y'),
                ha='center', va='center',
                fontsize=10,  # Tamaño de letra
                fontweight='bold')
        ax.text(x, y, '\n'.join(wrap_text(desc, 20)),
                ha='center', va='center',
                fontsize=10)  # Tamaño de letra

    # Eliminar ejes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Ajuste fijo del título y subtítulo en la parte superior izquierda
    subtitulo = "Línea de Vida - Terceros"

    fig.text(0.02, 0.98, 'NECTIM', 
            fontsize=40, color='black', 
            fontweight='bold', ha='left', va='top')
    fig.text(0.023, 0.91, subtitulo, 
            fontsize=14, color='black', 
            ha='left', va='top')

    plt.tight_layout()

    # Guardar el archivo como PDF si se activa la opción
    if guardar_pdf:
        # Obtener el nombre del archivo de la subcadena en el subtítulo
        nombre_archivo = f"C:\\HERRAMIENTAS\\Lineas de vida\\{subtitulo}.pdf"
        fig.savefig(nombre_archivo, format='pdf')

    return plt

def wrap_text(text, width):
    """Divide el texto en líneas"""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

# Ejemplo de uso
texto_ejemplo = """ CONFIRMAR
13/04/2023 PTE CONFIRMAR
12/04/2023 PTE CONFIRMAR
10/04/2023 PROGRAMAR TENDIDO
05/04/2023 TELEFONICA A SITIO
30/03/2023 TELEFONICA A SITIO
23/03/2023 APROBACION
16/03/2023 FECHA RTA
07/03/2023 PERSONAL TELEFONICA
06/03/2023 PROGRAMAR TENDIDO.
02/03/2023 PROXIMA SEMANA 
01/03/2023 PERSONAL EOC                      
28/02/2023 PROGRAMAR TENDIDO
23/02/2023 RTA TENTATIVA
"""

# Ruta de la imagen de fondo
imagen_fondo = "C:\\HERRAMIENTAS\\Fondo.jpeg"  # Cambia esto a la ruta real de tu imagen

# Crear y mostrar la línea de tiempo, y guardar como PDF
plt = crear_linea_tiempo_desarrollo(texto_ejemplo, imagen_fondo, guardar_pdf=True)
plt.show()
