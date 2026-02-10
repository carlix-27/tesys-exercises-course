// Consigna
// Pedir números hasta que se ingrese 0 
// e indicar cuántos números se ingresaron (sin contar el 0).

#include <stdio.h>

int main() {
    int num;
    int contador = 0;

    do {
        scanf("%d", &num);
        if (num != 0) {
            contador++;
        }
    } while (num != 0);

    printf("Cantidad de numeros ingresados: %d\n", contador);

    return 0;
}
