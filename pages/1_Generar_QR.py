import streamlit as st
import sys
import os

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

st.set_page_config(page_title="Generar QR", page_icon="🆔")

st.markdown("# Generar Código QR de Alumno")
st.write("Ingresa los datos del alumno para generar su tarjeta de identidad digital.")

with st.form("student_form"):
    student_id = st.text_input("Matrícula / ID del Estudiante")
    name = st.text_input("Nombre Completo")
    group_name = st.text_input("Grupo (Ej. 3A, 4B)")
    
    submitted = st.form_submit_button("Generar QR")

if submitted:
    if student_id and name and group_name:
        # Register student in DB (or update info)
        utils.register_student(student_id, name, group_name)
        
        # QR Content is just the Student ID
        qr_data = student_id
        qr_image = utils.generate_qr(qr_data)
        
        st.success(f"Código QR generado para **{name}** ({group_name})")
        
        # Display QR
        st.image(qr_image, caption=f"QR de {name}", width=300)
        
        # Download Button
        st.download_button(
            label="Descargar Código QR",
            data=qr_image,
            file_name=f"QR_{student_id}_{name.replace(' ', '_')}.png",
            mime="image/png"
        )
        
    else:
        st.error("Por favor completa todos los campos.")
