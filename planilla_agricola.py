import pandas as pd
import sys


def calcular_planilla(df):
    """Calcula la planilla agraria para un DataFrame de trabajadores."""
    resultados = []
    for _, fila in df.iterrows():
        salario_diario = fila['SalarioDiario']
        dias = fila['DiasTrabajados']
        horas_extra_25 = fila.get('HorasExtras25', 0)
        horas_extra_35 = fila.get('HorasExtras35', 0)

        # Sueldo básico
        sueldo_basico = salario_diario * dias

        # Valor de la hora normal
        valor_hora = salario_diario / 8.0

        # Pago de horas extras
        pago_extra_25 = horas_extra_25 * valor_hora * 1.25
        pago_extra_35 = horas_extra_35 * valor_hora * 1.35

        # Sueldo bruto
        sueldo_bruto = sueldo_basico + pago_extra_25 + pago_extra_35

        # Deducciones (9% salud, 13% pensión)
        deduccion_salud = sueldo_bruto * 0.09
        deduccion_pension = sueldo_bruto * 0.13
        total_deducciones = deduccion_salud + deduccion_pension

        # Sueldo neto
        sueldo_neto = sueldo_bruto - total_deducciones

        resultados.append({
            'Nombre': fila['Nombre'],
            'SueldoBasico': sueldo_basico,
            'PagoExtra25': pago_extra_25,
            'PagoExtra35': pago_extra_35,
            'SueldoBruto': sueldo_bruto,
            'DeduccionSalud': deduccion_salud,
            'DeduccionPension': deduccion_pension,
            'TotalDeducciones': total_deducciones,
            'SueldoNeto': sueldo_neto
        })

    return pd.DataFrame(resultados)


def main(archivo_entrada, archivo_salida):
    df = pd.read_csv(archivo_entrada)
    resultado = calcular_planilla(df)
    resultado.to_csv(archivo_salida, index=False)
    print(f"Planilla calculada guardada en {archivo_salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python planilla_agricola.py <entrada.csv> <salida.csv>")
        sys.exit(1)

    entrada = sys.argv[1]
    salida = sys.argv[2]
    main(entrada, salida)
