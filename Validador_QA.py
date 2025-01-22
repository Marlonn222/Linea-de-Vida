import pandas as pd
import os

def validate_codes(excel_path, folder_path):
    # Leer el archivo Excel
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return

    # Verificar si las columnas necesarias existen
    required_columns = ['CODIGO DE SERVICIO', 'STATU']
    for col in required_columns:
        if col not in df.columns:
            print(f"El archivo Excel no contiene la columna requerida: {col}")
            return

    # Obtener los códigos de la columna 'CODIGO DE SERVICIO'
    codes = df['CODIGO DE SERVICIO'].astype(str)  # Asegurar que sean strings

    # Obtener los nombres de los archivos en la carpeta
    try:
        file_names = os.listdir(folder_path)
    except Exception as e:
        print(f"Error al acceder a la carpeta: {e}")
        return

    # Crear una lista para almacenar los resultados
    results = []

    # Validar cada código
    for code in codes:
        exists = any(code in file_name for file_name in file_names)
        results.append("Existe" if exists else "No Existe")

    # Añadir los resultados a la columna 'STATUS'
    df['STATUS'] = results

    # Guardar el archivo Excel con los resultados
    output_path = excel_path.replace(".xlsx", "_validado.xlsx")
    try:
        df.to_excel(output_path, index=False)
        print(f"Archivo guardado con los resultados en: {output_path}")
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")

# Ruta del archivo Excel y la carpeta
excel_path = r"C:\Users\mabeb\Downloads\Input BOT 001 V1.xlsx"
folder_path = r"C:\Users\mabeb\Downloads\CONSOLIDADO GENERAL"

# Ejecutar la validación
validate_codes(excel_path, folder_path)
