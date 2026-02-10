// Consigna
// Pedir edades hasta que se ingrese -1.
// Mostrar cuántas personas son mayores de edad.

#include <stdio.h>

int main() {
    int edad;
    int mayores = 0;

    do {
        scanf("%d", &edad);
        if (edad >= 18) {
            mayores++;
        }
    } while (edad != -1);

    printf("Cantidad de mayores de edad: %d\n", mayores);

    return 0;
}
