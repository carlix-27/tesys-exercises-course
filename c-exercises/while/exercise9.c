// Consigna
// Pedir una nota válida (0 a 10).
// No permitir continuar hasta que sea correcta.

#include <stdio.h>

int main() {
    int nota;

    scanf("%d", &nota);

    while (nota < 0 || nota > 10) {
        printf("Nota invalida. Reintente\n");
        scanf("%d", &nota);
    }

    printf("Nota ingresada: %d\n", nota);

    return 0;
}
