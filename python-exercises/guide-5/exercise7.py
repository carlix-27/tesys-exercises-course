import os

FILENAME = "archivo.txt" 

# Este codigo, te genera el archivo con 5 lineas
# TODO: Podrias generalizarlo para poder recibir N lineas. 
lines = ["Linea 1", "Linea 2", "Linea 3", "Linea 4", "Linea 5", "Fin"]
with open(FILENAME, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

# ---------- 1. Leer y mostrar el archivo completo ----------
print("=" * 50) # ============================================ 
print("CONTENIDO COMPLETO DEL ARCHIVO")
print("=" * 50) 
with open(FILENAME, "r", encoding="utf-8") as f:
    contenido = f.read()
print(contenido)

# ---------- 2. Primeros 7 caracteres con seek() y tell() ----------
print("=" * 50)
print("PRIMEROS 7 CARACTERES (seek / tell)")
print("=" * 50)
with open(FILENAME, "rb") as f:   # modo binario para que seek/tell sean exactos en bytes
    for i in range(7):
        pos_antes = f.tell()
        caracter = f.read(1).decode("utf-8")
        pos_despues = f.tell()
        print(f"Posicion {pos_antes:>3} -> '{caracter}' (siguiente posicion: {pos_despues})")

# ---------- 3. Cada linea con su longitud ----------
print("=" * 50)
print("LINEAS Y CANTIDAD DE CARACTERES")
print("=" * 50)
with open(FILENAME, "r", encoding="utf-8") as f:
    for i, linea in enumerate(f, start=1):
        # strip() saca el \n para no contarlo; si querés contarlo usá len(linea)
        limpia = linea.rstrip("\n")
        print(f"Linea {i:>2}: '{limpia}' -> {len(limpia)} caracteres")

# ---------- 4. Añadir al final: total de caracteres del archivo ----------


total_chars = len(contenido)          # caracteres que ya leimos antes
nueva_linea = f"\nTotal de caracteres del archivo: {total_chars}\n"

with open(FILENAME, "a", encoding="utf-8") as f:
    f.write(nueva_linea)

print("=" * 50)
print(f"Se añadio al final: '{nueva_linea.strip()}'")
print("Archivo final:")
with open(FILENAME, "r", encoding="utf-8") as f:
    print(f.read())