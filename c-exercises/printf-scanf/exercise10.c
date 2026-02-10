// Consigna

// Pedir:
// nombre
// edad
// promedio
// Mostrar un mensaje completo usando todos los datos.

#include <stdio.h>

int main() {
    char nombre[30];
    int edad;
    float promedio;

    scanf("%s", nombre);
    scanf("%d", &edad);
    scanf("%f", &promedio);

    printf("El alumno %s tiene %d anios y un promedio de %.2f\n",
           nombre, edad, promedio);

    return 0;
}
