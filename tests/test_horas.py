from utils.hour_calculator import calcular_horas, procesar_fila


def test_diurna_sin_refrigerio():
    d, n = calcular_horas("08:00", "16:00")
    assert round(d, 2) == 8
    assert round(n, 2) == 0


def test_diurna_con_refrigerio():
    d, n = calcular_horas("08:00", "18:00", "13:00", "14:00")
    assert round(d, 2) == 9
    assert round(n, 2) == 0


def test_nocturna_sin_refrigerio():
    d, n = calcular_horas("22:00", "06:00")
    assert round(d, 2) == 0
    assert round(n, 2) == 8


def test_mixta_con_refrigerio():
    d, n = calcular_horas("20:00", "04:00", "00:00", "01:00")
    assert round(d, 2) == 2
    assert round(n, 2) == 5


def test_procesar_fila_basic():
    row = {
        "Hora Inicio Labores": "08:00",
        "Hora Término Labores": "18:00",
        "Hora Inicio Refrigerio": "13:00",
        "Hora Término Refrigerio": "14:00",
    }
    resultado = procesar_fila(row)
    assert resultado["Horas Diurnas"] == 9
    assert resultado["Horas Nocturnas"] == 0
    assert resultado["Total Horas"] == 9
