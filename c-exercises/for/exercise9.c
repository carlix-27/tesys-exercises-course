// Consigna
// Pedir 5 números y mostrar el mayor

#include <stdio.h>

int main() {
    int num;
    int max;
    int i;

    scanf("%d", &max);

    for (i = 1; i < 5; i++) {
        scanf("%d", &num);
        if (num > max) {
            max = num;
        }
    }

    printf("El mayor es: %d\n", max);

    return 0;
}
