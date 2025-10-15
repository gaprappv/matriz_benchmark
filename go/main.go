package main

import (
	"fmt"
	"math/rand"
	"os"
	"time"
)

func main() {
	var N, M1, M2, M3 = 100, 500, 1000, 2000
	rand.Seed(time.Now().UnixNano())
	os.MkdirAll("results", 0755)

	//exists := false
	//if _, err := os.Stat("results/benchmark.csv"); err == nil {
	//	exists = true
	//}

	f, err := os.OpenFile("results/benchmark.csv", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		fmt.Println("No se pudo abrir CSV:", err)
		return
	}
	defer f.Close()

	//if exists {
	//	f.WriteString("\n//******************************\n")
	//}

	//f.WriteString("repeticion,tiempo_segundos,cantidad_multiplicacion,tamano_matriz\n")

	A := make([][]int, N)
	B := make([][]int, N)
	C := make([][]int, N)
	for i := 0; i < N; i++ {
		A[i] = make([]int, N)
		B[i] = make([]int, N)
		C[i] = make([]int, N)
	}

	cantidades := []int{M1, M2, M3}

	for _, cantidad := range cantidades {
		for rep := 1; rep <= 5; rep++ {
			for i := 0; i < N; i++ {
				for j := 0; j < N; j++ {
					A[i][j] = rand.Intn(10)
					B[i][j] = rand.Intn(10)
					C[i][j] = 0
				}
			}

			start := time.Now()

			for i := 0; i < N; i++ {
				for j := 0; j < N; j++ {
					s := 0
					for k := 0; k < N; k++ {
						s += A[i][k] * B[k][j]
					}
					C[i][j] = s
				}
			}

			secs := time.Since(start).Seconds()
			f.WriteString(fmt.Sprintf("go,%d,%.6f,%d,%d\n", rep, secs, cantidad, N))
		}
	}
}
