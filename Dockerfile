FROM ubuntu:22.04

LABEL maintainer="Gonzalo Paredes"
LABEL description="Benchmark de matrices en C++/Go/Java/Python con Snakemake + ANOVA"
LABEL version="1.3"
LABEL repository="https://hub.docker.com/r/gapr1986/matriz_benchmark"

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 1) Herramientas y runtimes
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      g++ \
      clang \
      golang-go \
      openjdk-17-jdk \
      python3 \
      python3-pip \
      python3-venv \
      python3-yaml \
      ca-certificates \
      curl \
      git && \
    rm -rf /var/lib/apt/lists/*

# 2) Librerías científicas (evitamos compilar con pip)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3-pandas \
      python3-scipy \
      python3-matplotlib \
      python3-statsmodels && \
    rm -rf /var/lib/apt/lists/*

# 3) Snakemake por APT (suficiente para este pipeline)
RUN apt-get update && \
    apt-get install -y --no-install-recommends snakemake && \
    rm -rf /var/lib/apt/lists/*

# 4) Copiar código del proyecto
COPY cpp/     /app/cpp/
COPY go/      /app/go/
COPY java/    /app/java/
COPY python/  /app/python/
COPY run_all.py /app/

# 5) Copiar workflow + script ANOVA + config
COPY workflow/ /app/workflow/
COPY scripts/  /app/scripts/
COPY config/   /app/config/

# 6) Directorios de salida
RUN mkdir -p /app/results /app/analysis && \
    chmod 777 /app/results /app/analysis

# 7) No pre-compilamos aquí para evitar fallos; compila en runtime (run_all.py)
# RUN g++ -O2 -std=c++17 -o /app/cpp/main /app/cpp/main.cpp && javac /app/java/Main.java

# 8) Entrypoint: ejecuta el pipeline completo (bench -> anova)
ENTRYPOINT ["snakemake", "-j", "1"]