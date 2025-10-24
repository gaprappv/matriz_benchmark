import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm

csv_path   = snakemake.input["csv"]
anova_out  = snakemake.output["table"]
means_out  = snakemake.output["means"]
box_out    = snakemake.output["box"]
qq_out     = snakemake.output["qq"]
summary_out= snakemake.output["summary"]
formula    = snakemake.params["formula"]
outdir     = snakemake.params["outdir"]

os.makedirs(outdir, exist_ok=True)

# ---------- 1) Cargar CSV de forma robusta ----------
# - comment='/' descarta líneas que empiezan con '/' (incluye "//************")
# - skip_blank_lines=True ignora líneas vacías
# - engine='python' es más tolerante
df = pd.read_csv(
    csv_path,
    comment='/',
    skip_blank_lines=True,
    engine='python'
)

# Si el CSV tiene encabezados repetidos, esas filas quedan como filas de texto.
# Nos quedamos solo con las columnas esperadas. Si faltan, lanzamos error claro.
expected = ["lenguaje", "repeticion", "tiempo_segundos", "cantidad_multiplicacion", "tamano_matriz"]
missing = [c for c in expected if c not in df.columns]
if missing:
    raise ValueError(f"Faltan columnas en {csv_path}: {missing}. "
                     "Revisa que los programas escriban el header correcto.")

# Filtramos y renumeramos índice
df = df[expected].copy()

# ---------- 2) Limpieza de tipos ----------
# Strip en columnas string
df["lenguaje"] = df["lenguaje"].astype(str).str.strip()

# Forzamos tipos numéricos donde corresponde
for col in ["repeticion", "cantidad_multiplicacion", "tamano_matriz"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["tiempo_segundos"] = pd.to_numeric(df["tiempo_segundos"], errors="coerce")

# Quitamos filas inválidas
df = df.dropna(subset=["lenguaje", "repeticion", "tiempo_segundos", "cantidad_multiplicacion", "tamano_matriz"])

# Convertimos a categorías los factores del ANOVA
df["lenguaje"] = df["lenguaje"].astype("category")
df["cantidad_multiplicacion"] = df["cantidad_multiplicacion"].astype("category")

# ---------- 3) Guardar un CSV limpio para auditoría ----------
clean_path = os.path.join(outdir, "clean_benchmark.csv")
df.to_csv(clean_path, index=False)

# ---------- 4) Ajustar modelo OLS y ANOVA ----------
model = smf.ols(formula, data=df).fit()
anova_tbl = anova_lm(model, typ=2)
anova_tbl.to_csv(anova_out)

# ---------- 5) Medias por grupo ----------
means = (
    df.groupby(["lenguaje", "cantidad_multiplicacion"])["tiempo_segundos"]
      .agg(["count", "mean", "std"])
      .reset_index()
)
means.to_csv(means_out, index=False)

# ---------- 6) Figuras ----------
# Boxplot por lenguaje
plt.figure()
df.boxplot(column="tiempo_segundos", by="lenguaje")
plt.title("Distribución de tiempos por lenguaje")
plt.suptitle("")
plt.xlabel("Lenguaje")
plt.ylabel("Tiempo (s)")
plt.tight_layout()
plt.savefig(box_out, dpi=150)
plt.close()

# QQ-plot de residuos
fig = sm.qqplot(model.resid, line="45", fit=True)
plt.title("QQ-Plot de residuos")
plt.tight_layout()
plt.savefig(qq_out, dpi=150)
plt.close()

# ---------- 7) Resumen ----------
with open(summary_out, "w") as f:
    f.write(model.summary().as_text())
    f.write("\n\nANOVA (Type II):\n")
    f.write(anova_tbl.to_string())
