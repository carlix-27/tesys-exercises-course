// Consigna

// Pedir un número e indicar si:

// -> es múltiplo de 3 y 5
// -> solo de 3
// -> solo de 5
// -> ninguno

#include <stdio.h>

int main() {
    int num;

    scanf("%d", &num);

    if (num % 3 == 0 && num % 5 == 0) {
        printf("Multiplo de 3 y 5\n");
    } else if (num % 3 == 0) {
        printf("Multiplo de 3\n");
    } else if (num % 5 == 0) {
        printf("Multiplo de 5\n");
    } else {
        printf("No es multiplo de 3 ni de 5\n");
    }

    return 0;
}
