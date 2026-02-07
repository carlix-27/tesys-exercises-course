// Consigna
// Pedir un número del **1 al 3** y mostrar:

// - 1 → “Uno”
// - 2 → “Dos”
// - 3 → “Tres”
// - otro → “Número inválido”

#include <stdio.h>

int main() {
    int num;

    scanf("%d", &num);

    switch (num) {
        case 1:
            printf("Uno\n");
            break;
        case 2:
            printf("Dos\n");
            break;
        case 3:
            printf("Tres\n");
            break;
        default:
            printf("Numero invalido\n");
    }

    return 0;
}
