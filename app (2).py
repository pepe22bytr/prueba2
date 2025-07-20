import streamlit as st
import pandas as pd
import io
from utils.hour_calculator import (
    convertir_a_str,
    calcular_horas,
    procesar_fila,
    calcular_dia_tra,
)

def main():
    st.title("📊 Procesador de Horas Laborales")
    st.markdown("### Carga y procesa archivos Excel con datos de horas trabajadas")
    
    # Información sobre el formato esperado
    with st.expander("ℹ️ Formato de archivo esperado"):
        st.markdown("""
        **El archivo Excel debe contener una hoja llamada 'Horas' con las siguientes columnas:**
        - `DIA`: Día de la semana (lunes, martes, miércoles, jueves, viernes, sábado, domingo)
        - `Hora Inicio Labores`: Hora de inicio en formato HH:MM:SS
        - `Hora Término Labores`: Hora de término en formato HH:MM:SS
        - `Hora Inicio Refrigerio`: (Opcional) Hora de inicio del refrigerio
        - `Hora Término Refrigerio`: (Opcional) Hora de término del refrigerio
        
        **Cálculos realizados:**
        - Horas diurnas (06:00-22:00) y nocturnas (22:00-06:00)
        - Horas normales (hasta 8 horas) y extras
        - Sobretiempo con recargo del 25% y 35%
        - Tratamiento especial para domingos y feriados
        - Descuento automático de refrigerio (13:00-14:00)
        """)
    
    # Upload file
    uploaded_file = st.file_uploader(
        "📁 Selecciona el archivo Excel",
        type=['xlsx', 'xls'],
        help="Sube un archivo Excel con los datos de horas laborales"
    )
    
    if uploaded_file is not None:
        try:
            # Read the Excel file
            with st.spinner("📖 Leyendo archivo Excel..."):
                df = pd.read_excel(uploaded_file, sheet_name="Horas")
            
            st.success(f"✅ Archivo cargado exitosamente. {len(df)} filas encontradas.")
            
            # Display original data
            st.subheader("📋 Datos originales")
            st.dataframe(df, use_container_width=True)
            
            # Process data
            if st.button("🔄 Procesar datos", type="primary"):
                with st.spinner("⚙️ Procesando datos..."):
                    try:
                        # Apply processing to each row
                        resultados_dict = df.apply(procesar_fila, axis=1, result_type="expand")
                        
                        # Combine original data with results
                        df_final = pd.concat([df, resultados_dict], axis=1)
                        
                        st.success("✅ Datos procesados exitosamente!")
                        
                        # Display processed data
                        st.subheader("📊 Resultados calculados")
                        
                        # Show only the calculated columns for better readability
                        calculated_columns = [
                            "Horas Diurnas", "Horas Nocturnas", "Horas Normales",
                            "Extra 25%", "Extra 35%", "Extra 25% Nocturna", 
                            "Extra 35% Nocturna", "Total Horas",
                            "Horas Domingo/Feriado", "Horas Extra Domingo/Feriado"
                        ]
                        
                        # Display calculated results
                        st.dataframe(df_final[calculated_columns], use_container_width=True)
                        
                        # Summary statistics
                        st.subheader("📈 Resumen")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            total_horas_normales = df_final["Horas Normales"].sum()
                            st.metric("Total Horas Normales", f"{total_horas_normales:.2f}")
                        
                        with col2:
                            total_extra_25 = df_final["Extra 25%"].sum()
                            st.metric("Total Extra 25%", f"{total_extra_25:.2f}")
                        
                        with col3:
                            total_extra_35 = df_final["Extra 35%"].sum()
                            st.metric("Total Extra 35%", f"{total_extra_35:.2f}")
                        
                        with col4:
                            total_horas = df_final["Total Horas"].sum()
                            st.metric("Total Horas", f"{total_horas:.2f}")
                        
                        # Download processed file
                        st.subheader("💾 Descargar resultado")
                        
                        # Create Excel file in memory
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df_final.to_excel(writer, sheet_name='Horas_Procesadas', index=False)
                        
                        excel_data = output.getvalue()
                        
                        st.download_button(
                            label="📥 Descargar archivo procesado",
                            data=excel_data,
                            file_name="reporte_horas_procesado.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            help="Descarga el archivo Excel con todos los cálculos realizados"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error al procesar los datos: {str(e)}")
                        st.error("Verifica que el archivo tenga el formato correcto y las columnas requeridas.")
        
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {str(e)}")
            st.error("Asegúrate de que el archivo tenga una hoja llamada 'Horas' con el formato correcto.")
    
    else:
        st.info("👆 Por favor, sube un archivo Excel para comenzar el procesamiento.")
    
    # Footer
    st.markdown("---")
    st.markdown("📍 **Nota**: Este procesador calcula automáticamente las horas laborales según la legislación laboral peruana, incluyendo recargos por sobretiempo y trabajo nocturno.")

if __name__ == "__main__":
    main()
