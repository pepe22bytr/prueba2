import pandas as pd
from datetime import datetime


def convertir_a_str(value: object) -> str:
    """Devuelve una representacion en cadena de una hora.

    Si el valor es un objeto `Timestamp` o `datetime`, se formatea como
    ``HH:MM:SS``. Si el valor es NaN o ``None`` se retorna una cadena vacia.
    """
    if pd.isna(value):
        return ""
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.strftime("%H:%M:%S")
    return str(value)


def calcular_horas(hora_inicio: str, hora_fin: str) -> float:
    """Calcula la diferencia en horas entre dos horas en formato ``HH:MM:SS``."""
    fmt = "%H:%M:%S"
    inicio = datetime.strptime(hora_inicio, fmt)
    fin = datetime.strptime(hora_fin, fmt)
    delta = fin - inicio
    return delta.total_seconds() / 3600.0


def calcular_dia_tra(dia: object) -> str:
    """Normaliza el nombre del dia a capitalizacion estandar."""
    if not isinstance(dia, str):
        return str(dia)
    return dia.strip().capitalize()


def procesar_fila(fila: pd.Series) -> pd.Series:
    """Procesa una fila de un DataFrame y calcula las horas trabajadas.

    La fila debe contener las columnas:
    ``DIA``, ``Hora Inicio Labores`` y ``Hora Término Labores``. Si se
    proporcionan ``Hora Inicio Refrigerio`` y ``Hora Término Refrigerio``,
    se descontarán del total de horas.
    """
    inicio = convertir_a_str(fila.get("Hora Inicio Labores"))
    termino = convertir_a_str(fila.get("Hora Término Labores"))
    ref_ini = convertir_a_str(fila.get("Hora Inicio Refrigerio"))
    ref_fin = convertir_a_str(fila.get("Hora Término Refrigerio"))

    total_horas = 0.0
    if inicio and termino:
        total_horas = calcular_horas(inicio, termino)
    if ref_ini and ref_fin:
        total_horas -= calcular_horas(ref_ini, ref_fin)
        if total_horas < 0:
            total_horas = 0

    return pd.Series({
        "DIA": calcular_dia_tra(fila.get("DIA")),
        "Total Horas": round(total_horas, 2),
    })
