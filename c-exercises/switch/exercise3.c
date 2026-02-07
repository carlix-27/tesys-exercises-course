// Consigna
// Pedir una letra e indicar si es una vocal o no.

#include <stdio.h>

int main() {
    char letra;

    scanf(" %c", &letra);

    switch (letra) {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
            printf("Es vocal\n");
            break;
        default:
            printf("No es vocal\n");
    }

    return 0;
}
