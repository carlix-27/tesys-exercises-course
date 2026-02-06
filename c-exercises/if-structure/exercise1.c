// Consigna
// Pedir un número entero e indicar si es positivo o negativo.

#include <stdio.h>

int main() {
    int num;

    scanf("%d", &num);

    if (num >= 0) {
        printf("El numero es positivo\n");
    } else {
        printf("El numero es negativo\n");
    }

    return 0;
}
