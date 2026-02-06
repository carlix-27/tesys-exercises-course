// Consigna
// Pedir una nota (0 a 10).
// Si está fuera del rango, mostrar "Nota invalida".

#include <stdio.h>

int main() {
    int nota;

    scanf("%d", &nota);

    if (nota < 0 || nota > 10) {
        printf("Nota invalida\n");
    } else if (nota >= 6) {
        printf("Aprobado\n");
    } else {
        printf("Desaprobado\n");
    }

    return 0;
}
