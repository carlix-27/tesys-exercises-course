// Consigna
// Sumar los números del 1 al 10 y mostrar el resultado.

#include <stdio.h>

int main() {
    int suma = 0;
    int i;

    for (i = 1; i <= 10; i++) {
        suma += i;
    }

    printf("Suma total: %d\n", suma);

    return 0;
}
