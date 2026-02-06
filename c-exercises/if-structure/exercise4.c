// Consigna
// Pedir dos números e indicar cuál es mayor o si son iguales.

#include <stdio.h>

int main() {
    int a, b;

    scanf("%d %d", &a, &b);

    if (a > b) {
        printf("El mayor es %d\n", a);
    } else if (b > a) {
        printf("El mayor es %d\n", b);
    } else {
        printf("Los numeros son iguales\n");
    }

    return 0;
}
