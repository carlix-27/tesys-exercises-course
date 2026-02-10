// Consigna
// Pedir números y sumarlos hasta que se ingrese 0.

#include <stdio.h>

int main() {
    int num;
    int suma = 0;

    scanf("%d", &num);

    while (num != 0) {
        suma += num;
        scanf("%d", &num);
    }

    printf("Suma total: %d\n", suma);

    return 0;
}
