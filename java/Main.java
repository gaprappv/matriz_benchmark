import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        try {
            Scanner sc = new Scanner(System.in);

            int N = 100;
            int M1 = 500;
            int M2 = 1000;      
            int M3 = 2000;

            new File("results").mkdirs();
            File csvFile = new File("results/benchmark.csv");
            boolean exists = csvFile.exists();
            BufferedWriter bw = new BufferedWriter(new FileWriter(csvFile, true));

            //if (exists) {
            //    bw.write("\n//******************************\n");
            //}
            //bw.write("lenguaje,repeticion,tiempo_segundos,cantidad_multiplicacion,tamano_matriz\n");
            //bw.flush();

            Random rnd = new Random();
            int[][] A = new int[N][N];
            int[][] B = new int[N][N];
            int[][] C = new int[N][N];
            int[] cantidades = {M1, M2, M3};

            for (int cantidad : cantidades) {
                for (int rep = 1; rep <= 5; rep++) {
                    for (int i = 0; i < N; i++)
                        for (int j = 0; j < N; j++) {
                            A[i][j] = rnd.nextInt(10);
                            B[i][j] = rnd.nextInt(10);
                            C[i][j] = 0;
                        }

                    long t0 = System.nanoTime();
                    for (int i = 0; i < N; i++)
                        for (int j = 0; j < N; j++) {
                            int s = 0;
                            for (int k = 0; k < N; k++)
                                s += A[i][k] * B[k][j];
                            C[i][j] = s;
                        }
                    double secs = (System.nanoTime() - t0) / 1_000_000_000.0;
                    bw.write("java,"+ rep + "," + String.format(Locale.US, "%.6f", secs) + "," + cantidad + "," + N + "\n");
                    bw.flush();
                }
            }
            bw.close();
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}