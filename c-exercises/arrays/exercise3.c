// Consigna
// Cargar 5 números y mostrar la suma total.

#include <stdio.h>

int main() {
    int numeros[5];
    int suma = 0;
    int i;

    for (i = 0; i < 5; i++) {
        scanf("%d", &numeros[i]);
        suma += numeros[i];
    }

    printf("Suma total: %d\n", suma);

    return 0;
}
