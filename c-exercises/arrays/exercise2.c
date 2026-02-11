// Consigna
// Pedir 5 números al usuario y guardarlos en un array.

#include <stdio.h>

int main() {
    int numeros[5];
    int i;

    for (i = 0; i < 5; i++) {
        scanf("%d", &numeros[i]);
    }

    for (i = 0; i < 5; i++) {
        printf("%d\n", numeros[i]);
    }

    return 0;
}
