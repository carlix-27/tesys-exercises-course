// Consigna
// Pedir una nota (0 a 10) e indicar:

// -> Excelente (9 o 10)
// -> Aprobado (6 a 8)
// -> Desaprobado (menos de 6)


#include <stdio.h>

int main() {
    int nota;

    scanf("%d", &nota);

    if (nota >= 9) {
        printf("Excelente\n");
    } else if (nota >= 6) {
        printf("Aprobado\n");
    } else {
        printf("Desaprobado\n");
    }

    return 0;
}
