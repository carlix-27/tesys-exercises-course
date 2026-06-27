import csv

FILENAME = "tabla_alimentos.csv"  # cambia la ruta si hace falta

# ---------- Leer el CSV ----------
with open(FILENAME, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    filas = list(reader)           # lista de dicts; cada clave es un encabezado
    columnas = reader.fieldnames   # ['100 gramos de', 'Calorias', ...]

# Separar columnas numericas de la columna de nombre
col_nombre = columnas[0]
cols_numericas = columnas[1:]      # ['Calorias', 'Lipido', 'Proteina', ...]

# Convertir valores a float para operar
def to_float(valor):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None

# ---------- 1. Min / Promedio / Max por columna numerica ----------
print("=" * 65)
print(f"{'Columna':<25} {'Min':>8} {'Promedio':>12} {'Max':>8}")
print("=" * 65)

estadisticas = {}   # guardamos los promedios para el filtro posterior

for col in cols_numericas:
    valores = [to_float(fila[col]) for fila in filas if to_float(fila[col]) is not None]
    minimo  = min(valores)
    maximo  = max(valores)
    promedio = sum(valores) / len(valores)
    estadisticas[col] = promedio
    print(f"{col:<25} {minimo:>8.2f} {promedio:>12.2f} {maximo:>8.2f}")

# ---------- 2. Filtrar filas con ALGUN valor inferior a la media de su columna ----------
print("\n" + "=" * 65)
print("FILAS CON AL MENOS UN VALOR INFERIOR A LA MEDIA DE SU COLUMNA")
print("=" * 65)

filas_filtradas = []
for fila in filas:
    for col in cols_numericas:
        val = to_float(fila[col])
        if val is not None and val < estadisticas[col]:
            filas_filtradas.append(fila)
            break   # basta con que una columna cumpla la condicion

# Encabezado de la tabla filtrada
ancho_nombre = 28
print(f"\n{'Alimento':<{ancho_nombre}}", end="")
for col in cols_numericas:
    print(f"{col:>13}", end="")
print()
print("-" * (ancho_nombre + 13 * len(cols_numericas)))

for fila in filas_filtradas:
    print(f"{fila[col_nombre]:<{ancho_nombre}}", end="")
    for col in cols_numericas:
        val = to_float(fila[col])
        # Resaltar con * si el valor esta por debajo de la media
        marca = "*" if val is not None and val < estadisticas[col] else " "
        print(f"{str(val) + marca:>13}", end="")
    print()

print("\n* = valor inferior a la media de esa columna")
print(f"\nTotal filas originales   : {len(filas)}")
print(f"Total filas en resultado : {len(filas_filtradas)}")