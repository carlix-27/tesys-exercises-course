// Consigna
// Pedir un número entero y uno decimal, y mostrarlos.

#include <stdio.h>

int main() {
    int edad;
    float altura;

    scanf("%d %f", &edad, &altura);
    printf("Edad: %d\n", edad);
    printf("Altura: %.2f\n", altura);

    return 0;
}
