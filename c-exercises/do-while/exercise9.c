// Consigna
// Pedir una nota válida (0 a 10).
// No permitir salir hasta que sea correcta.

#include <stdio.h>

int main() {
    int nota;

    do {
        scanf("%d", &nota);
        if (nota < 0 || nota > 10) {
            printf("Nota invalida. Reintente\n");
        }
    } while (nota < 0 || nota > 10);

    printf("Nota ingresada: %d\n", nota);

    return 0;
}
