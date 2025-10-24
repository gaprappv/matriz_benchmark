#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_ROOT = ROOT / "results"

def run(cmd, cwd=None):
    print(f"\n$ {cmd}")
    r = subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd else None)
    if r.returncode != 0:
        print(f"[ERROR] '{cmd}' code={r.returncode}")
        sys.exit(r.returncode)

def run_list(args, cwd=None):
    print(f"\n$ {' '.join(args)}")
    r = subprocess.run(args, cwd=str(cwd) if cwd else None)
    if r.returncode != 0:
        print(f"[ERROR] '{' '.join(args)}' code={r.returncode}")
        sys.exit(r.returncode)

def ensure_dirs_and_links():
    # Asegura carpeta de resultados en la RAIZ
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)

    # En cada lenguaje, crear/forzar symlink "results" -> ../results
    for sub in ["cpp", "go", "java", "python"]:
        d = ROOT / sub
        link = d / "results"
        target = Path("..") / "results"  # relativo al subdir

        # borrar si existe algo con ese nombre
        if link.exists() or link.is_symlink():
            # forzamos limpieza (archivo, dir o symlink)
            run("rm -rf results", cwd=d)

        # crear symlink que apunta a ../results
        run(f"ln -s {target} results", cwd=d)

def main():
    ensure_dirs_and_links()
    print(">>> Ejecutando benchmarks (C++/Go/Java/Python) y escribiendo en results/benchmark.csv")

    # ---- C++ ----
    cpp_dir = ROOT / "cpp"
    cpp_src = cpp_dir / "main.cpp"
    cpp_exe = cpp_dir / "main"
    compiler = shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        print("No se encontró g++ ni clang++ en el contenedor.")
        sys.exit(1)
    run_list([compiler, "-O2", "-std=c++17", "-o", str(cpp_exe), str(cpp_src)], cwd=cpp_dir)
    run_list([str(cpp_exe)], cwd=cpp_dir)

    # ---- Go ----
    go_dir = ROOT / "go"
    run("go run main.go", cwd=go_dir)

    # ---- Java ----
    java_dir = ROOT / "java"
    run("javac Main.java", cwd=java_dir)
    run("java -cp . Main", cwd=java_dir)

    # ---- Python ----
    py_dir = ROOT / "python"
    run("python3 main.py", cwd=py_dir)

    # Verificación final: el CSV debe existir con contenido en /app/results
    bench = RESULTS_ROOT / "benchmark.csv"
    if not bench.exists() or bench.stat().st_size == 0:
        print("[ERROR] No se generó results/benchmark.csv con contenido en la raíz.")
        # Diagnóstico extra: listar posibles CSVs sueltos
        for sub in ["cpp", "go", "java", "python"]:
            p = ROOT / sub / "results" / "benchmark.csv"
            print(f"  - Chequeo {p}: {'OK' if p.exists() and p.stat().st_size>0 else 'no encontrado o vacío'}")
        sys.exit(1)

    print("\n>>> Benchmarks completados. Revisa results/benchmark.csv")

if __name__ == "__main__":
    main()