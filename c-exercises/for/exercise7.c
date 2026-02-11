// Consigna
// Pedir un número y calcular su factorial.

#include <stdio.h>

int main() {
    int num;
    int i;
    int factorial = 1;

    scanf("%d", &num);

    for (i = 1; i <= num; i++) {
        factorial *= i;
    }

    printf("Factorial: %d\n", factorial);

    return 0;
}
