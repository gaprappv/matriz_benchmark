import os
import subprocess

# Ruta base del proyecto
root = os.path.dirname(os.path.abspath(__file__))

print("=== Iniciando ejecución de los 4 programas ===")

# Crear carpeta results si no existe
os.makedirs(os.path.join(root, "results"), exist_ok=True)

# -----------------------------
# 1) Ejecutar C++
# -----------------------------
print("\nCompilando y ejecutando C++...")
cpp_exe = os.path.join(root, "cpp", "main")
cpp_src = os.path.join(root, "cpp", "main.cpp")

# Compila
subprocess.run(["clang++", "-O2", "-std=c++17", "-o", cpp_exe, cpp_src])

# Ejecuta
subprocess.run([cpp_exe])

# -----------------------------
# 2) Ejecutar Go
# -----------------------------
print("\nEjecutando Go...")
go_file = os.path.join(root, "go", "main.go")
subprocess.run(["go", "run", go_file])

# -----------------------------
# 3) Ejecutar Java
# -----------------------------
print("\nCompilando y ejecutando Java...")
java_src = os.path.join(root, "java", "Main.java")

# Compila
subprocess.run(["javac", java_src])

# Ejecuta
subprocess.run(["java", "-cp", os.path.join(root, "java"), "Main"])

# -----------------------------
# 4) Ejecutar Python
# -----------------------------
print("\nEjecutando Python...")
py_file = os.path.join(root, "python", "main.py")
subprocess.run(["python3", py_file])

print("\n=== Ejecución completa ===")
print("Los resultados se guardaron en: results/benchmark.csv")