// Consigna
// Cargar 10 números y contar cuántos son pares.

#include <stdio.h>

int main() {
    int numeros[10];
    int i;
    int contador = 0;

    for (i = 0; i < 10; i++) {
        scanf("%d", &numeros[i]);
    }

    for (i = 0; i < 10; i++) {
        if (numeros[i] % 2 == 0) {
            contador++;
        }
    }

    printf("Cantidad de pares: %d\n", contador);

    return 0;
}
