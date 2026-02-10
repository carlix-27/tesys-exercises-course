// Consigna
// Pedir números hasta ingresar 0 y mostrar el promedio.

#include <stdio.h>

int main() {
    int num;
    int suma = 0;
    int contador = 0;

    scanf("%d", &num);

    while (num != 0) {
        suma += num;
        contador++;
        scanf("%d", &num);
    }

    if (contador > 0) {
        printf("Promedio: %.2f\n", (float)suma / contador);
    } else {
        printf("No se ingresaron numeros\n");
    }

    return 0;
}
