// Consigna
// Cargar 5 números en un array y copiarlos en otro

#include <stdio.h>

int main() {
    int a[5];
    int b[5];
    int i;

    for (i = 0; i < 5; i++) {
        scanf("%d", &a[i]);
    }

    for (i = 0; i < 5; i++) {
        b[i] = a[i];
    }

    printf("Array copiado:\n");

    for (i = 0; i < 5; i++) {
        printf("%d\n", b[i]);
    }

    return 0;
}
