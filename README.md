# Planilla Agraria

Este repositorio contiene un ejemplo sencillo de cómo calcular la planilla (nómina) para trabajadores del régimen agrario. Incluye un script de Python que toma un archivo CSV con la información de los trabajadores y genera un nuevo archivo con los montos calculados.

## Requisitos
- Python 3.8 o superior
- Biblioteca `pandas`

Puedes instalar la dependencia ejecutando:

```bash
pip install pandas
```

## Uso
1. Prepara un archivo CSV con las siguientes columnas:
   - `Nombre`
   - `DiasTrabajados`
   - `SalarioDiario`
   - `HorasExtras25` (opcional)
   - `HorasExtras35` (opcional)

2. Ejecuta el script indicando el archivo de entrada y el de salida:

```bash
python planilla_agricola.py trabajadores.csv planilla_calculada.csv
```

Se generará un archivo `planilla_calculada.csv` con el detalle del sueldo básico, las horas extras, las deducciones y el sueldo neto de cada trabajador.

