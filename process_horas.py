"""Herramientas de procesamiento de archivos de horas."""

import pandas as pd
from utils.hour_calculator import (
    convertir_a_str,
    calcular_horas,
    procesar_fila,
    calcular_dia_tra,
)


def procesar_archivo(path: str) -> pd.DataFrame:
    """Lee un archivo de Excel y aplica ``procesar_fila`` a cada fila."""
    df = pd.read_excel(path, sheet_name="Horas")
    resultados = df.apply(procesar_fila, axis=1)
    return pd.concat([df, resultados], axis=1)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python process_horas.py <archivo.xlsx>")

    df_final = procesar_archivo(sys.argv[1])
    output = sys.argv[1].replace(".xlsx", "_procesado.xlsx")
    df_final.to_excel(output, index=False)
    print(f"Archivo procesado guardado en {output}")
