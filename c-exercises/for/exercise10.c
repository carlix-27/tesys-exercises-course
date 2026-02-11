// Consigna
// Mostrar un menú 3 veces usando for

#include <stdio.h>

int main() {
    int opcion;
    int i;

    for (i = 1; i <= 3; i++) {
        printf("1. Opcion A\n");
        printf("2. Opcion B\n");
        printf("3. Opcion C\n");

        scanf("%d", &opcion);

        printf("Elegiste la opcion %d\n", opcion);
    }

    return 0;
}
