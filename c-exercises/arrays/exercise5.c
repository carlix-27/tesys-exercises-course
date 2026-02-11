// Consigna
// Cargar 5 números y mostrar el mayor.

#include <stdio.h>

int main() {
    int numeros[5];
    int i;
    int mayor;

    for (i = 0; i < 5; i++) {
        scanf("%d", &numeros[i]);
    }

    mayor = numeros[0];

    for (i = 1; i < 5; i++) {
        if (numeros[i] > mayor) {
            mayor = numeros[i];
        }
    }

    printf("Mayor: %d\n", mayor);

    return 0;
}
