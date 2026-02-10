// Consigna
// Pedir un nombre (sin espacios) y mostrarlo.

#include <stdio.h>

int main() {
    char nombre[20];

    scanf("%s", nombre);
    printf("Hola %s!\n", nombre);

    return 0;
}

