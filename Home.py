import streamlit as st
import os

st.set_page_config(
    page_title="Sistema de Asistencia Escolar",
    page_icon="🏫",
)

st.write("# Bienvenido al Sistema de Asistencia Escolar! 👋")

st.sidebar.success("Selecciona una opción arriba.")

st.markdown(
    """
    Este sistema permite gestionar la asistencia de alumnos de manera eficiente mediante códigos QR.
    
    ### ¿Cómo funciona?
    
    1.  **Generar QR**: Los alumnos (o el maestro) pueden ingresar sus datos y generar un código QR único.
        Este código debe ser guardado por el alumno.
    2.  **Escanear QR**: El maestro utiliza esta opción para escanear el código QR del alumno desde su dispositivo
        móvil o computadora con cámara. Esto registra la asistencia automáticamente.
    3.  **Estadísticas**: Visualiza los registros de asistencia y filtra por fecha o grupo.
    
    ### Empezar
    
    Selecciona **Generar QR** en el menú de la izquierda para comenzar a registrar alumnos, o **Escanear QR** para
    tomar asistencia si ya tienes los códigos generados.
    """
)
