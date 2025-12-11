import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import sys
import os

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

st.set_page_config(page_title="Escanear QR", page_icon="📷")

st.markdown("# Escanear Asistencia")
st.write("Permite el acceso a la cámara y muestra el código QR del alumno.")

img_file_buffer = st.camera_input("Capturar QR")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    
    # Use Pillow to open image, then convert to array
    image = Image.open(img_file_buffer)
    img_array = np.array(image)
    
    # Decode QR
    decoded_objects = decode(img_array)
    
    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            st.info(f"Código detectado: {qr_data}")
            
            # Try to record attendance
            success, message = utils.record_attendance(qr_data)
            
            if success:
                st.success(message)
                st.balloons()
            else:
                st.warning(message)
                
            # Break after first detection to avoid multiple rapid fires
            break
    else:
        st.error("No se detectó ningún código QR. Intenta acercar más la imagen o mejorar la iluminación.")

