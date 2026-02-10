// Consigna
// Pedir un número hasta que sea positivo.

#include <stdio.h>

int main() {
    int num;

    do {
        scanf("%d", &num);
    } while (num <= 0);

    printf("Numero valido: %d\n", num);

    return 0;
}
