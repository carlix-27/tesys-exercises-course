// Consigna

// Pedir dos números y una opción:

// 1 → suma
// 2 → resta
// 3 → multiplicación
// 4 → división

#include <stdio.h>

int main() {
    int op;
    float a, b;

    scanf("%f %f", &a, &b);
    scanf("%d", &op);

    switch (op) {
        case 1:
            printf("Resultado: %.2f\n", a + b);
            break;
        case 2:
            printf("Resultado: %.2f\n", a - b);
            break;
        case 3:
            printf("Resultado: %.2f\n", a * b);
            break;
        case 4:
            if (b != 0)
                printf("Resultado: %.2f\n", a / b);
            else
                printf("No se puede dividir por cero\n");
            break;
        default:
            printf("Opcion invalida\n");
    }

    return 0;
}
