#include <iostream>
#include <vector>
#include <fstream>
#include <ctime>
#include <cstdlib>
#include <sys/stat.h>

int main() {
    // Parametrización simple y fija para desbloquear el pipeline
    int N = 100;
    int cantidades[3] = {500, 1000, 2000};

    std::srand((unsigned)std::time(nullptr));

    // Asegura carpeta results dentro del contenedor (por si no existe)
    system("mkdir -p results");

    // Si el archivo ya existe, escribe separador como pediste
    bool exists = false;
    {
        std::ifstream check("results/benchmark.csv");
        if (check.good()) exists = true;
    }

    std::ofstream csv("results/benchmark.csv", std::ios::app);
    if (exists) {
        csv << "\n//******************************\n";
    } else {
        // Header que espera el ANOVA
        csv << "lenguaje,repeticion,tiempo_segundos,cantidad_multiplicacion,tamano_matriz\n";
    }

    // Matrices
    std::vector<std::vector<int>> A(N, std::vector<int>(N));
    std::vector<std::vector<int>> B(N, std::vector<int>(N));
    std::vector<std::vector<int>> C(N, std::vector<int>(N));

    // Recorremos las 3 cantidades y repetimos 5 veces cada una
    for (int idx = 0; idx < 3; idx++) {
        int cantidad = cantidades[idx];
        for (int rep = 1; rep <= 5; rep++) {

            // Rellenar matrices con 0..9
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    A[i][j] = std::rand() % 10;
                    B[i][j] = std::rand() % 10;
                    C[i][j] = 0;
                }
            }

            // Tiempo total de UNA multiplicación A x B (no por iteración interna)
            clock_t start = clock();

            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    int s = 0;
                    for (int k = 0; k < N; k++) {
                        s += A[i][k] * B[k][j];
                    }
                    C[i][j] = s;
                }
            }

            clock_t end = clock();
            double secs = double(end - start) / CLOCKS_PER_SEC;

            // Escribir una fila por repetición
            csv << "c++," << rep << "," << secs << "," << cantidad << "," << N << "\n";
        }
    }

    csv.close();
    std::cout << "C++ listo\n";
    return 0;
}
