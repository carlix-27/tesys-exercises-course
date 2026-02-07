// Consigna

// Pedir una opción (1–3) y un número.
// Según la opción:

// 1 -> Cuadrado

// 2 -> Cubo

// 3 -> Doble

#include <stdio.h>

int main() {
    int opcion;
    int num;

    scanf("%d", &opcion);
    scanf("%d", &num);

    switch (opcion) {
        case 1:
            printf("Cuadrado: %d\n", num * num);
            break;
        case 2:
            printf("Cubo: %d\n", num * num * num);
            break;
        case 3:
            printf("Doble: %d\n", num * 2);
            break;
        default:
            printf("Opcion invalida\n");
    }

    return 0;
}
