// Consigna
// Cargar 5 números y luego pedir otro número para indicar si está en el array.

#include <stdio.h>

int main() {
    int numeros[5];
    int i;
    int buscado;
    int encontrado = 0;

    for (i = 0; i < 5; i++) {
        scanf("%d", &numeros[i]);
    }

    scanf("%d", &buscado);

    for (i = 0; i < 5; i++) {
        if (numeros[i] == buscado) {
            encontrado = 1;
        }
    }

    if (encontrado) {
        printf("Numero encontrado\n");
    } else {
        printf("Numero no encontrado\n");
    }

    return 0;
}
