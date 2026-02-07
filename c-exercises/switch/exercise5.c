// Consigna

// Pedir una letra:

// A → Excelente
// B → Muy bien
// C → Bien
// D → Insuficiente

#include <stdio.h>

int main() {
    char nota;

    scanf(" %c", &nota);

    switch (nota) {
        case 'A':
            printf("Excelente\n");
            break;
        case 'B':
            printf("Muy bien\n");
            break;
        case 'C':
            printf("Bien\n");
            break;
        case 'D':
            printf("Insuficiente\n");
            break;
        default:
            printf("Nota invalida\n");
    }

    return 0;
}
