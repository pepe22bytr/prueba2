import streamlit as st
import pandas as pd
from io import BytesIO

from payroll_calculator import process_dataframe


def main() -> None:
    st.title("Payroll Calculator")
    st.write("Upload an Excel file to calculate payroll metrics.")

    uploaded_file = st.file_uploader("Excel file", type=["xlsx", "xls"])
    sheet_name = st.text_input("Sheet name", "Sheet1")

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            st.success("File loaded successfully")
            st.dataframe(df.head())

            if st.button("Calculate"):
                with st.spinner("Processing..."):
                    results = process_dataframe(df)
                st.subheader("Results")
                st.dataframe(results)

                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    results.to_excel(writer, index=False)

                st.download_button(
                    "Download Excel",
                    data=buffer.getvalue(),
                    file_name="resultados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        except Exception as exc:
            st.error(f"Error processing file: {exc}")


if __name__ == "__main__":
    main()
