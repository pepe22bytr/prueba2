from datetime import datetime, timedelta
from typing import Optional, Tuple

TIME_FORMATS = ["%H:%M:%S", "%H:%M"]

def _parse_time(value: str) -> datetime:
    for fmt in TIME_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Formato de hora invalido: {value}")


def calcular_horas(hora_inicio: str, hora_fin: str,
                   hora_inicio_ref: Optional[str] = None,
                   hora_fin_ref: Optional[str] = None) -> Tuple[float, float]:
    """Calcula horas diurnas y nocturnas considerando refrigerio."""
    start = _parse_time(hora_inicio)
    end = _parse_time(hora_fin)
    if end <= start:
        end += timedelta(days=1)

    trabajo_inicio = start
    trabajo_fin = end

    # Ajustar por refrigerio
    if hora_inicio_ref and hora_fin_ref:
        ref_start = _parse_time(hora_inicio_ref)
        ref_end = _parse_time(hora_fin_ref)
        if ref_end <= ref_start:
            ref_end += timedelta(days=1)
        if ref_start < start:
            ref_start += timedelta(days=1)
            ref_end += timedelta(days=1)
        # si el refrigerio esta dentro del rango de trabajo
        if ref_start < trabajo_fin and ref_end > trabajo_inicio:
            if ref_start > trabajo_inicio:
                inicio_intervalo = trabajo_inicio
                fin_intervalo = ref_start
                diurnas, nocturnas = _calcular_intervalo(inicio_intervalo, fin_intervalo)
            else:
                diurnas = nocturnas = 0
            d2, n2 = _calcular_intervalo(ref_end, trabajo_fin)
            diurnas += d2
            nocturnas += n2
            return diurnas, nocturnas
    # Sin refrigerio
    return _calcular_intervalo(trabajo_inicio, trabajo_fin)


def _calcular_intervalo(inicio: datetime, fin: datetime) -> Tuple[float, float]:
    diurnas = 0.0
    nocturnas = 0.0
    current = inicio
    while current < fin:
        next_point = min(fin, current.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))
        if next_point <= current:
            next_point = current + timedelta(hours=1)
        tramo = (next_point - current).total_seconds() / 3600
        hora_actual = current.time()
        if 6 <= hora_actual.hour < 22:
            diurnas += tramo
        else:
            nocturnas += tramo
        current = next_point
    return diurnas, nocturnas


def procesar_fila(row):
    diurnas, nocturnas = calcular_horas(
        str(row.get("Hora Inicio Labores")),
        str(row.get("Hora Término Labores")),
        str(row.get("Hora Inicio Refrigerio")) if row.get("Hora Inicio Refrigerio") not in [None, "nan"] else None,
        str(row.get("Hora Término Refrigerio")) if row.get("Hora Término Refrigerio") not in [None, "nan"] else None,
    )
    return {
        "Horas Diurnas": round(diurnas, 2),
        "Horas Nocturnas": round(nocturnas, 2),
        "Total Horas": round(diurnas + nocturnas, 2),
    }
