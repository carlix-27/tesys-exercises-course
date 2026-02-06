// Consigna

// Pedir la edad de una persona e indicar:

// - Niño (menor de 12)
// - Adolescente (12 a 17)
// - Adulto (18 a 64)
// - Adulto mayor (65 o más)

#include <stdio.h>

int main() {
    int edad;

    scanf("%d", &edad);

    if (edad < 12) {
        printf("Niño\n");
    } else if (edad < 18) {
        printf("Adolescente\n");
    } else if (edad < 65) {
        printf("Adulto\n");
    } else {
        printf("Adulto mayor\n");
    }

    return 0;
}
