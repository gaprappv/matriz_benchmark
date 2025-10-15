#include <iostream>
#include <vector>
#include <fstream>
#include <ctime>
#include <cstdlib>
#include <sys/stat.h>

int main() {
    int N = 100;
    int M1=500, M2=1000, M3=2000;

    std::srand((unsigned)std::time(nullptr));

    system("mkdir -p results");

    bool exists = false;
    std::ifstream check("results/benchmark.csv");
    if (check.good()) exists = true;
    check.close();

    std::ofstream csv("results/benchmark.csv", std::ios::app);
    if (exists) {
        csv << "\n//******************************\n";
    }
    csv << "lenguaje,repeticion,tiempo_segundos,cantidad_multiplicacion,tamano_matriz\n";

    std::vector<std::vector<int>> A(N, std::vector<int>(N));
    std::vector<std::vector<int>> B(N, std::vector<int>(N));
    std::vector<std::vector<int>> C(N, std::vector<int>(N));

    int cantidades[3] = {M1, M2, M3};

    for (int idx = 0; idx < 3; idx++) {
        int cantidad = cantidades[idx];
        for (int rep = 1; rep <= 5; rep++) {
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    A[i][j] = std::rand() % 10;
                    B[i][j] = std::rand() % 10;
                    C[i][j] = 0;
                }
            }

            clock_t start = clock();
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++) {
                    int s = 0;
                    for (int k = 0; k < N; k++)
                        s += A[i][k] * B[k][j];
                    C[i][j] = s;
                }
            clock_t end = clock();
            double secs = double(end - start) / CLOCKS_PER_SEC;

            csv << "c++," << rep << "," << secs << "," << cantidad << "," << N << "\n";
        }
    }

    csv.close();
    return 0;
}
