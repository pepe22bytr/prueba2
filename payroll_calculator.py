"""Payroll calculation script.

This script reads an Excel file with payroll data and computes
various compensation metrics. The result is written to a new
Excel file.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def load_data(path: Path, sheet: str) -> pd.DataFrame:
    """Load an Excel sheet into a DataFrame."""
    excel = pd.ExcelFile(path)
    if sheet not in excel.sheet_names:
        raise ValueError(f"Sheet '{sheet}' not found. Available: {excel.sheet_names}")
    return excel.parse(sheet)


# Calculation functions -----------------------------------------------------

I_DIARES = 1
N_SUEMIN = 1130
J_ASIFAM = 113
N_PORAGR = 0.06
N_GRAAGR = 16.66
N_CTSAGR = 9.72
N_FHESIM = 1.25
N_FHEEXC = 1.35
N_HORLAB = 8


def calcular_jornal_basico(j_sueldo, i_hordiu, i_hornoc):
    return ((j_sueldo / 8) * (i_hordiu + i_hornoc)).round(2)


def calcular_asignacion_familiar(j_asifam, i_hordiu, i_hornoc, i_hofern,
                                 i_ddmedi, i_dspate, i_licgoc, p_vacper):
    base = i_hordiu + i_hornoc + i_hofern + (i_ddmedi + i_dspate + i_licgoc + p_vacper) * 8
    if I_DIARES == 1:
        return ((j_asifam / 240) * base).round(2)
    adicional = (i_hordiu + i_hornoc + i_hofern + (i_dspate * 8) + (i_ddmedi * 8) + (i_licgoc * 8) + (p_vacper * 8)) / 6
    return ((j_asifam / 240) * (base + adicional)).round(2)


def calcular_descanso_medico(j_sueldo, i_ddmedi):
    return (j_sueldo * i_ddmedi).round(2)


def calcular_licencia_por_enfermedad(i_basub1, i_dsenfe):
    return (i_basub1 * i_dsenfe).round(2)


def calcular_dominical_descanso(i_diares, j_sueldo, i_hordiu, i_hornoc, i_hofern,
                                i_dsenfe, p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc):
    if i_diares == 1:
        return 0
    base = i_hordiu + i_hornoc + i_hofern + ((i_dsenfe + p_vacper + i_ddmedi + i_dsmate + i_dspate + i_licgoc) * 8)
    return ((j_sueldo / 48) * base).round(2)


def calcular_descanso_pre_post_natal(j_sueldo, i_dsmate):
    return (j_sueldo * i_dsmate).round(2)


def calcular_licencia_por_paternidad(j_sueldo, i_dspate):
    return (j_sueldo * i_dspate).round(2)


def calcular_horas_extras_25(j_sueldo, j_asifam, n_fhesim, i_hed25):
    return ((((j_sueldo / 8) + (j_asifam / 240)) * n_fhesim) * i_hed25).round(2)


def calcular_horas_extras_35(j_sueldo, j_asifam, n_fheexc, i_hed35):
    return ((((j_sueldo / 8) + (j_asifam / 240)) * n_fheexc) * i_hed35).round(2)


def calcular_horas_extras_25_noct(j_sueldo, j_asifam, n_fhesim, i_hed25_noct):
    return ((((j_sueldo / 8) + (j_asifam / 240)) * n_fhesim) * i_hed25_noct).round(2)


def calcular_horas_extras_35_noct(j_sueldo, j_asifam, n_fheexc, i_hed35_noct):
    return ((((j_sueldo / 8) + (j_asifam / 240)) * n_fheexc) * i_hed35_noct).round(2)


def calcular_feriados(j_sueldo, i_hofern):
    return ((j_sueldo / 8) * i_hofern).round(2)


def calcular_horas_nocturnas(j_sueldo, n_suemin, n_horlab, i_hornoc):
    if (j_sueldo > (n_suemin * 1.35 / 30)).any():
        return ((((n_suemin * 1.35 / 30) - j_sueldo) / n_horlab) * i_hornoc).round(2)
    return 0


def calcular_horas_feriados_100(j_sueldo, j_asifam, i_hf200):
    return ((((j_sueldo / 8) + (j_asifam / 240)) * 2) * i_hf200).round(2)


def calcular_horas_feriados_150(j_sueldo, j_asifam, i_hf250):
    return ((((j_sueldo / 8) + (j_asifam / 240)) * 2.5) * i_hf250).round(2)


def calcular_licencia_con_goce_de_habe(j_sueldo, i_licgoc):
    return (j_sueldo * i_licgoc).round(2)


def calcular_bonificacion_beta(n_suemin, i_hordiu, i_hornoc, i_hofern, i_dsenfe,
                               p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc,
                               i_diares):
    base = i_hordiu + i_hornoc + i_hofern + ((i_dsenfe + p_vacper + i_ddmedi + i_dsmate + i_dspate + i_licgoc) * 8)
    if i_diares == 1:
        return (((n_suemin * 0.30) / 240) * base).round(2)
    adicional = (i_hordiu + i_hornoc + i_hofern + (i_dsmate * 8) + (i_dspate * 8) + (i_dsenfe * 8) + (i_ddmedi * 8) + (i_licgoc * 8) + (p_vacper * 8)) / 6
    return (((n_suemin * 0.30) / 240) * (base + adicional)).round(2)


def calcular_gratificacion_navidad(j_sueldo, j_asifam, n_graagr, i_hordiu, i_hornoc, i_hofern,
                                   i_dsenfe, p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc):
    base = i_hordiu + i_hornoc + i_hofern + ((i_dsenfe + p_vacper + i_ddmedi + i_dsmate + i_dspate + i_licgoc) * 8)
    return ((((j_sueldo / 8) + (j_asifam / 240)) * (n_graagr / 100)) * base).round(2)


def calcular_bonificacion_extraordinaria(f_grtagr, n_poragr):
    return (f_grtagr * n_poragr).round(2)


def calcular_compensacion_tiempo_servicio(j_sueldo, j_asifam, n_ctsagr, i_hordiu, i_hornoc,
                                          i_hofern, i_dsenfe, p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc):
    base = i_hordiu + i_hornoc + i_hofern + ((i_dsenfe + p_vacper + i_ddmedi + i_dsmate + i_dspate + i_licgoc) * 8)
    return ((((j_sueldo / 8) + (j_asifam / 240)) * (n_ctsagr / 100)) * base).round(2)


# Main ----------------------------------------------------------------------

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    j_sueldo = df['SUELDO BASICO']
    i_hordiu = df['HORAS DIURNAS']
    i_hornoc = df['HORAS NOCTURNAS']
    i_hofern = df['HORAS FERIADO']
    i_hed25 = df['HE 25']
    i_hed35 = df['HE 35']
    i_hed25_noct = df['HE 25 NOCT']
    i_hed35_noct = df['HE 35 NOCT']
    i_ddmedi = df['DESCANSO MEDICO']
    i_dsenfe = df['DIAS SUBSIDIOS ENFERMEDAD']
    p_vacper = df['DIAS VACACIONES']
    i_licgoc = df['DIAS LICENCIAS CON GOCE']
    i_hf200 = df['HE 200']
    i_hf250 = df['HE 250']
    i_dspate = df['DIAS PATERNIDAD']
    i_dsmate = df['DIAS MATERNIDAD']
    i_basub1 = df['BASE SUBSIDIOS']

    resultados = pd.DataFrame({
        'Jornal Básico': calcular_jornal_basico(j_sueldo, i_hordiu, i_hornoc),
        'Descanso Médico': calcular_descanso_medico(j_sueldo, i_ddmedi),
        'Licencia por Enfermedad': calcular_licencia_por_enfermedad(i_basub1, i_dsenfe),
        'Dominical Descanso': calcular_dominical_descanso(I_DIARES, j_sueldo, i_hordiu, i_hornoc, i_hofern, i_dsenfe, p_vacper,
                                                        i_ddmedi, i_dsmate, i_dspate, i_licgoc),
        'Descanso Pre y Post Natal': calcular_descanso_pre_post_natal(j_sueldo, i_dsmate),
        'Licencia por Paternidad': calcular_licencia_por_paternidad(j_sueldo, i_dspate),
        'Horas Extras 25%': calcular_horas_extras_25(j_sueldo, J_ASIFAM, N_FHESIM, i_hed25),
        'Horas Extras 35%': calcular_horas_extras_35(j_sueldo, J_ASIFAM, N_FHEEXC, i_hed35),
        'Horas Extras 25% Nocturnas': calcular_horas_extras_25_noct(j_sueldo, J_ASIFAM, N_FHESIM, i_hed25_noct),
        'Horas Extras 35% Nocturnas': calcular_horas_extras_35_noct(j_sueldo, J_ASIFAM, N_FHEEXC, i_hed35_noct),
        'Bonificación Extraordinaria': calcular_bonificacion_extraordinaria(
            calcular_gratificacion_navidad(j_sueldo, J_ASIFAM, N_GRAAGR, i_hordiu, i_hornoc, i_hofern,
                                           i_dsenfe, p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc),
            N_PORAGR),
        'Feriados': calcular_feriados(j_sueldo, i_hofern),
        'Horas Nocturnas': calcular_horas_nocturnas(j_sueldo, N_SUEMIN, N_HORLAB, i_hornoc),
        'Horas Feriados 100%': calcular_horas_feriados_100(j_sueldo, J_ASIFAM, i_hf200),
        'Horas Feriados 150%': calcular_horas_feriados_150(j_sueldo, J_ASIFAM, i_hf250),
        'Licencia con Goce de Haberes': calcular_licencia_con_goce_de_habe(j_sueldo, i_licgoc),
        'Bonificación Beta': calcular_bonificacion_beta(N_SUEMIN, i_hordiu, i_hornoc, i_hofern, i_dsenfe,
                                                       p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc, I_DIARES),
        'Gratificación': calcular_gratificacion_navidad(j_sueldo, J_ASIFAM, N_GRAAGR, i_hordiu, i_hornoc,
                                                       i_hofern, i_dsenfe, p_vacper, i_ddmedi, i_dsmate, i_dspate, i_licgoc),
        'Compensación por Tiempo de Servicio': calcular_compensacion_tiempo_servicio(
            j_sueldo, J_ASIFAM, N_CTSAGR, i_hordiu, i_hornoc, i_hofern, i_dsenfe, p_vacper,
            i_ddmedi, i_dsmate, i_dspate, i_licgoc)
    })

    return resultados


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate payroll metrics from an Excel file")
    parser.add_argument("excel_file", type=Path, help="Path to the input Excel file")
    parser.add_argument("--sheet", default="Sheet1", help="Name of the sheet to read")
    parser.add_argument("--output", default="resultados.xlsx", help="Name of the output Excel file")
    args = parser.parse_args()

    df = load_data(args.excel_file, args.sheet)
    resultados = process_dataframe(df)
    resultados.to_excel(args.output, index=False)
    print(f"Resultados guardados en {args.output}")


if __name__ == "__main__":
    main()
