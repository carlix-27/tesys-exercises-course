// Consigna
// Pedir dos números y mostrar el resultado de todas las operaciones en una sola línea.

#include <stdio.h>

int main() {
    int a, b;

    scanf("%d %d", &a, &b);

    printf("Suma: %d | Resta: %d | Producto: %d\n",
           a + b, a - b, a * b);

    return 0;
}
