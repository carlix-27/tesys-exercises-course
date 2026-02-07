// Consigna

// Simular un menú de sistema:

// 1. Crear usuario
// 2. Editar usuario
// 3. Eliminar usuario
// 4. Salir

#include <stdio.h>

int main() {
    int opcion;

    printf("1. Crear usuario\n");
    printf("2. Editar usuario\n");
    printf("3. Eliminar usuario\n");
    printf("4. Salir\n");

    scanf("%d", &opcion);

    switch (opcion) {
        case 1:
            printf("Usuario creado\n");
            break;
        case 2:
            printf("Usuario editado\n");
            break;
        case 3:
            printf("Usuario eliminado\n");
            break;
        case 4:
            printf("Saliendo del sistema\n");
            break;
        default:
            printf("Opcion invalida\n");
    }

    return 0;
}
