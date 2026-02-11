// Consigna 
// Mostrar cuántos números pares hay del 1 al 100.

#include <stdio.h>

int main() {
    int contador = 0;
    int i;

    for (i = 1; i <= 100; i++) {
        if (i % 2 == 0) {
            contador++;
        }
    }

    printf("Cantidad de pares: %d\n", contador);

    return 0;
}
