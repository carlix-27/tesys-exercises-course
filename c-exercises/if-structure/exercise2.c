// Consigna
// Pedir un número e indicar si es par o impar.

#include <stdio.h>

int main() {
    int num;

    scanf("%d", &num);

    if (num % 2 == 0) {
        printf("El numero es par\n");
    } else {
        printf("El numero es impar\n");
    }

    return 0;
}
