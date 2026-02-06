// Consigna

// Pedir el sueldo de una persona e indicar:

// - Sueldo invalido (≤ 0)
// - Sueldo bajo (< 100000)
// - Sueldo medio (100000 a 250000)
// - Sueldo alto (> 250000)

#include <stdio.h>

int main() {
    float sueldo;

    scanf("%f", &sueldo);

    if (sueldo <= 0) {
        printf("Sueldo invalido\n");
    } else if (sueldo < 100000) {
        printf("Sueldo bajo\n");
    } else if (sueldo <= 250000) {
        printf("Sueldo medio\n");
    } else {
        printf("Sueldo alto\n");
    }

    return 0;
}
