// Consigna
// Pedir edades hasta ingresar -1.
// Mostrar cuántas personas son menores de edad.


#include <stdio.h>

int main() {
    int edad;
    int menores = 0;

    scanf("%d", &edad);

    while (edad != -1) {
        if (edad < 18) {
            menores++;
        }
        scanf("%d", &edad);
    }

    printf("Cantidad de menores de edad: %d\n", menores);

    return 0;
}
