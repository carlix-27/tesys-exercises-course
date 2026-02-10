// Consigna
// Mostrar un menú hasta que el usuario elija salir (opción 4).

#include <stdio.h>

int main() {
    int opcion;

    do {
        printf("1. Opcion A\n");
        printf("2. Opcion B\n");
        printf("3. Opcion C\n");
        printf("4. Salir\n");

        scanf("%d", &opcion);

        switch (opcion) {
            case 1:
                printf("Elegiste A\n");
                break;
            case 2:
                printf("Elegiste B\n");
                break;
            case 3:
                printf("Elegiste C\n");
                break;
            case 4:
                printf("Saliendo...\n");
                break;
            default:
                printf("Opcion invalida\n");
        }
    } while (opcion != 4);

    return 0;
}
