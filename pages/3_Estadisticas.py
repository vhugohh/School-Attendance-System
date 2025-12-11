import streamlit as st
import pandas as pd
import sys
import os

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

st.set_page_config(page_title="Estadísticas", page_icon="📊")

st.markdown("# Estadísticas de Asistencia")

df = utils.get_attendance_data()

if not df.empty:
    # Basic metrics
    total_records = len(df)
    unique_students = df['id'].nunique()
    
    col1, col2 = st.columns(2)
    col1.metric("Total de Asistencias", total_records)
    col2.metric("Alumnos Únicos", unique_students)
    
    st.divider()
    
    # Filters
    st.subheader("Filtrar Datos")
    
    # Date filter
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    dates = df['timestamp'].dt.date.unique()
    selected_date = st.selectbox("Seleccionar Fecha", options=['Todas'] + list(dates))
    
    filtered_df = df.copy()
    if selected_date != 'Todas':
        filtered_df = filtered_df[filtered_df['timestamp'].dt.date == selected_date]
        
    # Group filter
    groups = df['group_name'].unique()
    selected_group = st.selectbox("Seleccionar Grupo", options=['Todos'] + list(groups))
    
    if selected_group != 'Todos':
        filtered_df = filtered_df[filtered_df['group_name'] == selected_group]

    # Summary per Student
    st.subheader("Resumen por Alumno")
    summary_df = filtered_df.groupby(['id', 'name', 'group_name']).size().reset_index(name='Asistencias')
    st.dataframe(summary_df, use_container_width=True)

    st.divider()

    # Display Data
    st.subheader("Registro Detallado")

    st.dataframe(filtered_df, use_container_width=True)
    
    # Download
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Descargar CSV",
        csv,
        "asistencia.csv",
        "text/csv",
        key='download-csv'
    )
    
else:
    st.info("No hay registros de asistencia aún.")
