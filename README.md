
# Análisis del Índice de Precios al Consumidor (IPC) por Divisiones - Argentina

Este proyecto realiza una limpieza, transformación y preparación de los datos del IPC por divisiones para su uso en herramientas de visualización como Looker Studio o Power BI. Los datos provienen de series publicadas por INDEC y están disponibles como datos abiertos.

## Estructura del Proyecto

```
ipc_divisiones/
├── data/
│   ├── raw/                      # Datos originales CSV descargados
│   │   └── serie_ipc_divisiones.csv
│   ├── processed/               # Datos limpios listos para uso
│   │   └── ipc_divisiones_limpio.csv
│   └── output/                  # Salidas para visualización
│       ├── ipc_pivot.csv        # Formato ancho (wide)
│       ├── ipc_long.csv         # Formato largo (long)
│       └── log_duplicados.csv   # Duplicados detectados por fecha/división
│       └── log_nan_long.csv     # Valores nulos detectados en formato long
├── scripts/
│   └── procesar_ipc.py          # Script principal de procesamiento
├── notebooks/
│   └── preview_ipc.ipynb        # Exploración y gráficos
└── README.md
```

## Requisitos

- Python 3.8+
- pandas
- Jupyter Notebook (opcional para visualización previa)

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución del procesamiento

Desde la raíz del proyecto:

```bash
python scripts/procesar_ipc.py
```

Esto generará archivos limpios en `data/processed` y formatos compatibles con Looker Studio o Power BI en `data/output`.

## Visualización

- `ipc_pivot.csv`: Formato ancho por división y tipo de variación.
- `ipc_long.csv`: Recomendado para Looker Studio y Power BI. Incluye columnas:
  - `fecha`
  - `division`
  - `tipo_variacion` (mensual o interanual)
  - `valor`

## Fuente de los datos

Datos abiertos del INDEC disponibles en:
[https://www.indec.gob.ar](https://www.indec.gob.ar)

[Índices y variaciones porcentuales mensuales e interanuales según divisiones de la canasta, bienes y servicios, y clasificación de grupos. Diciembre de 2016-mayo de 2025](https://www.indec.gob.ar/ftp/cuadros/economia/serie_ipc_divisiones.csv)

## Licencia

MIT License
