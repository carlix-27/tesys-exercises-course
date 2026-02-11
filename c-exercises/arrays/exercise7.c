// Consigna
// Cargar 5 números y mostrarlos en orden inverso.

#include <stdio.h>

int main() {
    int numeros[5];
    int i;

    for (i = 0; i < 5; i++) {
        scanf("%d", &numeros[i]);
    }

    for (i = 4; i >= 0; i--) {
        printf("%d\n", numeros[i]);
    }

    return 0;
}
