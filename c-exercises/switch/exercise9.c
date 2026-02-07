// Consigna

// Pedir un número del 1 al 3 y mostrar:

// Si es 1 → “Basico”
// Si es 2 → “Intermedio”
// Si es 3 → “Avanzado”

#include <stdio.h>

int main() {
    int nivel;

    scanf("%d", &nivel);

    switch (nivel) {
        case 3:
            printf("Avanzado\n");
            break;
        case 2:
            printf("Intermedio\n");
            break;
        case 1:
            printf("Basico\n");
            break;
        default:
            printf("Nivel invalido\n");
    }

    return 0;
}
