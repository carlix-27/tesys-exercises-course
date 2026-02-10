// Consigna
// Pedir números hasta ingresar 0 y mostrar cuántos números se ingresaron.

#include <stdio.h>

int main() {
    int num;
    int contador = 0;

    scanf("%d", &num);

    while (num != 0) {
        contador++;
        scanf("%d", &num);
    }

    printf("Cantidad de numeros: %d\n", contador);

    return 0;
}
