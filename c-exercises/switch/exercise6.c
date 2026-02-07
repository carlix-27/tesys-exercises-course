// Consigna

// Mostrar un menú:

//1. Ver saldo

//2. Depositar

//3. Retirar

//4. Salir

// Pedir una opción y mostrar el mensaje correspondiente.

#include <stdio.h>

int main() {
    int opcion;

    printf("1. Ver saldo\n");
    printf("2. Depositar\n");
    printf("3. Retirar\n");
    printf("4. Salir\n");

    scanf("%d", &opcion);

    switch (opcion) {
        case 1:
            printf("Mostrando saldo...\n");
            break;
        case 2:
            printf("Depositar dinero...\n");
            break;
        case 3:
            printf("Retirar dinero...\n");
            break;
        case 4:
            printf("Saliendo...\n");
            break;
        default:
            printf("Opcion invalida\n");
    }

    return 0;
}
