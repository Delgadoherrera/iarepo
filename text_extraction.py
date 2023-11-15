from pdf2image import convert_from_bytes as pdf2image_convert_from_bytes
from io import BytesIO
import requests
import os
from PIL import Image, ImageFilter
from pytesseract import image_to_string
from pdfminer.high_level import extract_text
import base64
import imghdr

# [Funciones de extracción de texto]
# Aquí incluyes todas las funciones de extracción de texto: preprocess_image, extract_text_from_image, get_text_from_files, get_text_from_url, get_text_from_base64
def preprocess_image(image):
    image = image.convert('1').filter(ImageFilter.MedianFilter(size=3))
    width, height = image.size
    return image.resize((width * 2, height * 2), Image.BICUBIC)

# Función para extraer texto de una imagen utilizando OCR (Reconocimiento Óptico de Caracteres)
def extract_text_from_image(image):
    image = preprocess_image(image)
    return image_to_string(image)

def get_text_from_files(files):
    raw_text = ""
    for file in files:
        _, file_extension = os.path.splitext(file)
        if file_extension.lower() in ['.pdf']:
            extracted_text = extract_text(file).strip()
            if len(extracted_text) > 50:
                raw_text += " " + extracted_text
            else:
                images_from_pdf = pdf2image_convert_from_bytes(file)
                raw_text += " " + " ".join([extract_text_from_image(image) for image in images_from_pdf])
        elif file_extension.lower() in ['.tif', '.png', '.jpg', '.jpeg']:
            with open(file, "rb") as f:
                image = Image.open(f)
                raw_text += " " + extract_text_from_image(image)
        else:
            print(f"Formato de archivo no soportado: {file}")
    return raw_text.strip()

def get_text_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error al acceder a la URL: Código de estado {response.status_code}"

    content_type = response.headers.get('Content-Type', '')
    if 'pdf' in content_type:
        pdf_bytes = response.content
        images_from_pdf = pdf2image_convert_from_bytes(BytesIO(pdf_bytes))
        return " ".join([extract_text_from_image(image) for image in images_from_pdf])
    elif any(ext in content_type for ext in ['jpeg', 'png', 'jpg']):
        image = Image.open(BytesIO(response.content))
        return extract_text_from_image(image)
    else:
        return "Tipo de contenido no soportado: " + content_type

# Función para obtener texto desde datos en formato base64 (principalmente imágenes)
def get_text_from_base64(base64_data):
    try:
        # Decodificar los datos base64
        decoded_data = base64.b64decode(base64_data)

        # Revisar si los datos decodificados son una imagen
        if imghdr.what(None, h=decoded_data):
            # Procesar como imagen
            image = Image.open(BytesIO(decoded_data))
            return extract_text_from_image(image)
        else:
            # Procesar como PDF, pasando bytes directamente
            return " ".join([extract_text_from_image(image) for image in pdf2image_convert_from_bytes(decoded_data)])
    except Exception as e:
        print(f"Error al procesar los datos en base64: {str(e)}")
        return ""
def process_files(files, url, base64_data):
    if url:
        return get_text_from_url(url)
    elif base64_data:
        return get_text_from_base64(base64_data)
    else:
        return get_text_from_files(files)