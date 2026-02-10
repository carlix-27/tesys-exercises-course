// Consigna
// Pedir números hasta ingresar 0 y mostrar el promedio.

#include <stdio.h>

int main() {
    int num;
    int suma = 0;
    int contador = 0;

    do {
        scanf("%d", &num);
        if (num != 0) {
            suma += num;
            contador++;
        }
    } while (num != 0);

    if (contador > 0) {
        printf("Promedio: %.2f\n", (float)suma / contador);
    } else {
        printf("No se ingresaron numeros\n");
    }

    return 0;
}
