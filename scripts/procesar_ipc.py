import os
import pandas as pd

# Definir rutas
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
archivo_entrada = os.path.join(base_dir, 'data', 'raw', 'serie_ipc_divisiones.csv')
archivo_limpio = os.path.join(base_dir, 'data', 'processed', 'ipc_divisiones_limpio.csv')
archivo_pivot = os.path.join(base_dir, 'data', 'output', 'ipc_pivot.csv')
archivo_long = os.path.join(base_dir, 'data', 'output', 'ipc_long.csv')
archivo_nan_log = os.path.join(base_dir, 'data', 'output', 'log_nan_long.csv')

# Leer archivo
df = pd.read_csv(archivo_entrada, encoding='latin1', sep=';')

# Limpiar nombres de columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Transformar fecha desde 'periodo'
if 'periodo' in df.columns:
    df['fecha'] = df['periodo'].astype(str) + '01'  # ejemplo: 201612 → 20161201
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y%m%d', errors='coerce')
    df.drop(columns=['periodo'], inplace=True)

# Renombrar y filtrar
df_filtrado = df[["fecha", "descripcion", "v_m_ipc", "v_i_a_ipc", "region"]].copy()
df_filtrado = df_filtrado.rename(columns={
    "descripcion": "division",
    "v_m_ipc": "variacion_mensual",
    "v_i_a_ipc": "variacion_interanual"
})

# Convertir a numérico
df_filtrado["variacion_mensual"] = pd.to_numeric(df_filtrado["variacion_mensual"], errors='coerce')
df_filtrado["variacion_interanual"] = pd.to_numeric(df_filtrado["variacion_interanual"], errors='coerce')

# Guardar archivo limpio
os.makedirs(os.path.dirname(archivo_limpio), exist_ok=True)
df_filtrado.to_csv(archivo_limpio, index=False)
print(f"✅ Archivo limpio guardado en: {archivo_limpio}")

# Agrupar por fecha, división y región
df_grouped = df_filtrado.groupby(["fecha", "division", "region"], as_index=False).agg({
    "variacion_mensual": "mean",
    "variacion_interanual": "mean"
})

# Filtrar Nacional
df_nacional = df_grouped[df_grouped["region"] == "Nacional"]

# Pivotear (formato ancho)
pivot_mensual = df_nacional.pivot(index="fecha", columns="division", values="variacion_mensual")
pivot_interanual = df_nacional.pivot(index="fecha", columns="division", values="variacion_interanual")

# Renombrar columnas
pivot_mensual.columns = [f"{col}_mensual" for col in pivot_mensual.columns]
pivot_interanual.columns = [f"{col}_interanual" for col in pivot_interanual.columns]

# Unir y guardar pivoteado
pivot_total = pd.concat([pivot_mensual, pivot_interanual], axis=1).sort_index()
os.makedirs(os.path.dirname(archivo_pivot), exist_ok=True)
pivot_total.to_csv(archivo_pivot, index=True)
print(f"✅ Archivo pivoteado guardado en: {archivo_pivot}")

# Crear formato long
df_long = pd.melt(
    df_nacional,
    id_vars=["fecha", "division"],
    value_vars=["variacion_mensual", "variacion_interanual"],
    var_name="tipo_variacion",
    value_name="valor"
)

# Asegurar que valor sea numérico
df_long["valor"] = pd.to_numeric(df_long["valor"], errors="coerce")

# Eliminar filas sin datos
nan_rows = df_long[df_long["valor"].isna()]
if not nan_rows.empty:
    nan_rows.to_csv(archivo_nan_log, index=False)
    print(f"⚠️ Se encontraron valores vacíos. Guardado log en: {archivo_nan_log}")

df_long = df_long.dropna(subset=["valor"])

# Guardar archivo long
df_long.to_csv(archivo_long, index=False)
print(f"📄 Archivo en formato long guardado en: {archivo_long}")
