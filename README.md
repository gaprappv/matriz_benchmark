# Benchmark de Multiplicación de Matrices con Snakemake y ANOVA

Este proyecto ejecuta un benchmark de multiplicación de matrices utilizando cuatro lenguajes de programación (C++, Go, Java y Python). Posteriormente, los resultados se analizan mediante ANOVA utilizando Snakemake como orquestador del flujo de ejecución. Los resultados incluyen métricas numéricas y gráficos estadísticos.

---

## 1. Requisitos previos

Para ejecutar esta imagen es necesario contar únicamente con **Docker** instalado.  
Guía oficial de instalación: https://docs.docker.com/get-docker/

No es necesario instalar compiladores, Python, Go, Java ni Snakemake en el sistema operativo local.

---

## 2. Descarga de la imagen desde Docker Hub

Ejecutar el siguiente comando:

```bash
docker pull gapr1986/matriz_benchmark_snakemake:latest
```

---

## 3. Ejecución por sistema operativo

Antes de ejecutar, cree los directorios donde se almacenarán los resultados:

**Linux / macOS**
```bash
mkdir -p results analysis
```

**Windows PowerShell**
```powershell
mkdir results
mkdir analysis
```

### 3.1 Linux (x86_64)

```bash
docker run --rm \
  -v "$PWD/results:/app/results" \
  -v "$PWD/analysis:/app/analysis" \
  gapr1986/matriz_benchmark_snakemake:latest
```

### 3.2 Windows PowerShell (x86_64)

```powershell
docker run --rm `
  -v "${PWD}\results:/app/results" `
  -v "${PWD}\analysis:/app/analysis" `
  gapr1986/matriz_benchmark_snakemake:latest
```

### 3.3 macOS Intel (x86_64)

```bash
docker run --rm \
  -v "$PWD/results:/app/results" \
  -v "$PWD/analysis:/app/analysis" \
  gapr1986/matriz_benchmark_snakemake:latest
```

### 3.4 macOS Apple Silicon (M1/M2/M3 – ARM)

```bash
docker run --rm --platform linux/amd64 \
  -v "$PWD/results:/app/results" \
  -v "$PWD/analysis:/app/analysis" \
  gapr1986/matriz_benchmark_snakemake:latest
```

Nota: La bandera `--platform linux/amd64` es necesaria debido a que la imagen fue construida sobre dicha arquitectura para maximizar compatibilidad.

---

## 4. Resultados generados

Luego de la ejecución, se generarán archivos en los siguientes directorios locales:

```
results/
└── benchmark.csv

analysis/
├── anova_table.csv
├── group_means.csv
├── model_summary.txt
├── boxplot.png
├── residuals_qq.png
└── clean_benchmark.csv
```

- `benchmark.csv`: resultados crudos de tiempo por lenguaje
- `anova_table.csv`: tabla ANOVA
- `model_summary.txt`: resumen estadístico del modelo
- `boxplot.png`: distribución comparativa del tiempo de ejecución
- `residuals_qq.png`: gráfico de normalidad del modelo
- `clean_benchmark.csv`: datos filtrados utilizados en el análisis

---

## 5. Ejecución repetida y mantenimiento

Para una nueva ejecución, basta con volver a ejecutar el comando `docker run`.  
Si se desea limpiar resultados previos:

**Linux / macOS**
```bash
rm -rf results/* analysis/*
```

**Windows PowerShell**
```powershell
del results\* /Q
del analysis\* /Q
```

---

## 6. Notas de compatibilidad

- La imagen es compatible con cualquier sistema que soporte Docker
- En equipos Apple Silicon (ARM), es obligatorio utilizar `--platform linux/amd64`
- No se requiere instalar dependencias adicionales en el sistema anfitrión

---

## 7. Licencia

Este proyecto se distribuye bajo licencia MIT.

---

## 8. Contacto

Para dudas o mejoras, contactar a: **gaprappv**

---

