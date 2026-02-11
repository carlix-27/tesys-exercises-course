// Consigna
// Pedir un número y mostrar su tabla del 1 al 10.

#include <stdio.h>

int main() {
    int num;
    int i;

    scanf("%d", &num);

    for (i = 1; i <= 10; i++) {
        printf("%d x %d = %d\n", num, i, num * i);
    }

    return 0;
}
