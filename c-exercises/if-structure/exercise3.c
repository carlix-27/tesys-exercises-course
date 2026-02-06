// Consigna

// Pedir un número e indicar si es:
// -> positivo
// -> negativo
// -> cero

#include <stdio.h>

int main() {
    int num;

    scanf("%d", &num);

    if (num > 0) {
        printf("El numero es positivo\n");
    } else if (num < 0) {
        printf("El numero es negativo\n");
    } else {
        printf("El numero es cero\n");
    }

    return 0;
}
