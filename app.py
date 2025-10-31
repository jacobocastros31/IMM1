import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Conversor de Texto a Audio para Sordomudos",
    page_icon="🔊",
    layout="centered"
)

# --- TÍTULO E IMAGEN PRINCIPAL ---
st.title("🗣️ Conversor de Texto a Audio para Personas Sordomudas")
st.write(
    "Convierte cualquier texto escrito en audio para facilitar la comunicación con personas sordomudas. "
    "Simplemente escribe lo que deseas decir y genera una versión en voz clara y natural."
)

image = Image.open("Sordomudo.jpg")
st.image(image, width=350)

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("📝 Instrucciones Rápidas")
    st.write("1. Escribe el texto que deseas convertir en la caja de texto.")
    st.write("2. Selecciona el idioma en el que deseas escucharlo.")
    st.write("3. Presiona **Convertir a Audio** para generar el resultado.")

# --- CREAR CARPETA TEMPORAL ---
if not os.path.exists("temp"):
    os.mkdir("temp")

# --- SECCIÓN PRINCIPAL ---
st.subheader("🎧 Generador de Audio")

text = st.text_area("Escribe el texto que quieres convertir en audio:", placeholder="Ejemplo: Hola, ¿cómo estás?")
option_lang = st.selectbox("Selecciona el idioma del audio:", ("Español", "English"))

# --- ASIGNAR IDIOMA ---
if option_lang == "Español":
    lg = 'es'
else:
    lg = 'en'

# --- FUNCIÓN PRINCIPAL ---
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    file_name = text[:20].strip().replace(" ", "_") or "audio"
    file_path = f"temp/{file_name}.mp3"
    tts.save(file_path)
    return file_path

# --- BOTÓN DE CONVERSIÓN ---
if st.button("🔊 Convertir a Audio"):
    if text.strip() == "":
        st.warning("Por favor, escribe algún texto antes de convertirlo.")
    else:
        file_path = text_to_speech(text, lg)
        st.success("✅ Conversión completada exitosamente.")
        st.markdown("### Escucha tu audio:")
        st.audio(file_path, format="audio/mp3")

        # --- DESCARGAR ARCHIVO ---
        with open(file_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">📥 Descargar Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

# --- LIMPIAR ARCHIVOS ANTIGUOS ---
def remove_old_files(days):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    max_age = days * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - max_age:
            os.remove(f)
            print(f"Archivo eliminado: {f}")

remove_old_files(7)
