// Consigna
// Cargar 5 números y mostrar el promedio.

#include <stdio.h>

int main() {
    int numeros[5];
    int suma = 0;
    int i;

    for (i = 0; i < 5; i++) {
        scanf("%d", &numeros[i]);
        suma += numeros[i];
    }

    printf("Promedio: %.2f\n", (float)suma / 5);

    return 0;
}
