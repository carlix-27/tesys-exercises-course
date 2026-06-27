def fibonacci(n):
    """Genera los n primeros numeros de Fibonacci."""
    secuencia = []
    a, b = 0, 1
    for _ in range(n):
        secuencia.append(a)
        a, b = b, a + b
    return secuencia

# ---------- Entrada del usuario ----------
while True:
    try:
        n = int(input("Cuantos numeros de Fibonacci desea generar? "))
        if n <= 0:
            print("El valor debe ser mayor a 0.")
        else:
            break
    except ValueError:
        print("Ingrese un numero entero valido.")

nombre_archivo = input("Nombre del archivo de salida (sin extension): ").strip()
if not nombre_archivo:
    nombre_archivo = "fibonacci"
nombre_archivo += ".txt"

# ---------- Generar y guardar ----------
serie = fibonacci(n)

with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write(f"Serie de Fibonacci - primeros {n} terminos\n")
    f.write("=" * 40 + "\n")
    for i, num in enumerate(serie, start=1):
        f.write(f"F({i:>4}) = {num}\n")

# ---------- Mostrar resultado ----------
print(f"\nSerie generada y guardada en '{nombre_archivo}':")
with open(nombre_archivo, "r", encoding="utf-8") as f:
    print(f.read())