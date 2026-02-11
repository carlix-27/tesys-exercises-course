// Consigna
// Cargar 8 notas y mostrar:
// -> promedio
// -> cantidad de aprobados (>= 6)

#include <stdio.h>

int main() {
    float notas[8];
    float suma = 0;
    int aprobados = 0;
    int i;

    for (i = 0; i < 8; i++) {
        scanf("%f", &notas[i]);
        suma += notas[i];

        if (notas[i] >= 6) {
            aprobados++;
        }
    }

    printf("Promedio: %.2f\n", suma / 8);
    printf("Aprobados: %d\n", aprobados);

    return 0;
}
