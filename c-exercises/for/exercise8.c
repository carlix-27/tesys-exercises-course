// Consigna
// Pedir 5 números y mostrar el promedio.

#include <stdio.h>

int main() {
    int num;
    int suma = 0;
    int i;

    for (i = 1; i <= 5; i++) {
        scanf("%d", &num);
        suma += num;
    }

    printf("Promedio: %.2f\n", (float)suma / 5);

    return 0;
}
