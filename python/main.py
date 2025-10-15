import time, random, os, csv

N = 100
M1 = 500
M2 = 1000
M3 = 2000

os.makedirs("results", exist_ok=True)
csv_path = "results/benchmark.csv"
exists = os.path.exists(csv_path)

with open(csv_path, "a", newline="") as f:
    w = csv.writer(f)
    #if exists:
    #    f.write("\n//******************************\n")
    #w.writerow(["lenguaje", "repeticion", "tiempo_segundos", "cantidad_multiplicacion", "tamano_matriz"])

A = [[0]*N for _ in range(N)]
B = [[0]*N for _ in range(N)]
C = [[0]*N for _ in range(N)]
cantidades = [M1, M2, M3]

for cantidad in cantidades:
    for rep in range(1, 6):
        for i in range(N):
            for j in range(N):
                A[i][j] = random.randint(0, 9)
                B[i][j] = random.randint(0, 9)
                C[i][j] = 0

        t0 = time.time()
        for i in range(N):
            for j in range(N):
                s = 0
                for k in range(N):
                    s += A[i][k] * B[k][j]
                C[i][j] = s
        secs = time.time() - t0

        with open(csv_path, "a", newline="") as f2:
            w2 = csv.writer(f2)
            w2.writerow(["python",rep, f"{secs:.6f}", cantidad, N])
