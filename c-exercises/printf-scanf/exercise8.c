// Consigna

// Pedir:
// -> nombre
// -> edad
// -> altura

// Y mostrar los datos.

#include <stdio.h>

int main() {
    char nombre[20];
    int edad;
    float altura;

    scanf("%s", nombre);
    scanf("%d", &edad);
    scanf("%f", &altura);

    printf("Nombre: %s\n", nombre);
    printf("Edad: %d\n", edad);
    printf("Altura: %.2f\n", altura);

    return 0;
}
