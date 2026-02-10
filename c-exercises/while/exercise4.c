// Consigna
// Pedir un número mayor a 0.
// Si no cumple, volver a pedirlo.

#include <stdio.h>

int main() {
    int num;

    scanf("%d", &num);

    while (num <= 0) {
        scanf("%d", &num);
    }

    printf("Numero valido: %d\n", num);

    return 0;
}
