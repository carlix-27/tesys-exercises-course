// Consigna
// Pedir números y sumarlos hasta que el usuario ingrese 0.

#include <stdio.h>

int main() {
    int num;
    int suma = 0;

    do {
        scanf("%d", &num);
        suma += num;
    } while (num != 0);

    printf("Suma total: %d\n", suma);

    return 0;
}
