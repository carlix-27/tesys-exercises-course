// Consigna

// Pedir:

// -> edad
// -> si trabaja (1 = sí, 0 = no)

// Indicar:
// Menor de edad
// Adulto desempleado
// Adulto trabajador

#include <stdio.h>

int main() {
    int edad;
    int trabaja;

    scanf("%d", &edad);
    scanf("%d", &trabaja);

    if (edad < 18) {
        printf("Menor de edad\n");
    } else if (trabaja == 1) {
        printf("Adulto trabajador\n");
    } else {
        printf("Adulto desempleado\n");
    }

    return 0;
}
