
from unum_ia_api import app
import sys
import os
import pytest
import base64

ruta_del_directorio = os.path.abspath(os.path.join(__file__, '../../'))
imageBase64 = 'imageBase64.txt'
pdfBase64 = 'pdfBase64.txt'


print('IMAGEBASE64', imageBase64)
sys.path.insert(0, ruta_del_directorio)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_pdf_upload(client):
    data = {
        'question': 'A nombre de quien esta el documento?',
        'file': (open('/home/southatoms/Escritorio/unitaryTest/unumIA/src/test/filesTest/Certificado Camara de Comercio  AIO 26 oct  2023.pdf', 'rb'), 'archivo.pdf')
    }
    response = client.post('/ia/api/assets/answer', data=data)
    response_data_decoded = response.data.decode('utf-8')
    assert response_data_decoded == "El documento está a nombre de AIO VIRTUAL S.A.S."
    # Agrega más aserciones para validar la respuesta


def test_image_upload(client):
    data = {
        'question': 'A nombre de quien esta el documento?',
        'file': (open('/home/southatoms/Escritorio/unitaryTest/unumIA/src/test/filesTest/pruebaFactura.jpeg', 'rb'), 'imagen.jpg')
    }
    response = client.post('/ia/api/assets/answer', data=data)
    response_data_decoded = response.data.decode('utf-8')
    assert response_data_decoded == 'El documento está a nombre de "SEGUROS DE VIDA SURAMERICANA S.A."'
    # Agrega más aserciones para validar la respuesta


def test_base64_image(client):
    with open("imageBase64.txt", "r") as image_file:
        base64_string = image_file.read().strip()
    data = {
        'question': 'Monto de la factura',
        'base64_image': base64_string
    }
    response = client.post('/ia/api/assets/answer', data=data)
    response_data_decoded = response.data.decode('utf-8')
    assert response_data_decoded == 'El monto total de la factura es de 199.65 €.'


def test_base64_pdf(client):
    with open('pdfBase64.txt', "r") as pdf_file:
        base64_string = pdf_file.read().strip()  # Leer el string Base64
    data = {
        'question': 'A nombre de quien esta la factura?',
        'base64_image': base64_string  # Usar directamente el string Base64
    }
    response = client.post('/ia/api/assets/answer', data=data)
    response_data_decoded = response.data.decode('utf-8')
    assert response_data_decoded == 'La factura está a nombre de Florez Hernandez Saabi.'


def test_url(client):
    data = {
        'question': 'Monto de la factura?',
        'url': 'https://templates.invoicehome.com/modelo-factura-es-mono-negro-750px.png'
    }
    response = client.post('/ia/api/assets/answer', data=data)
    response_data_decoded = response.data.decode('utf-8')
    assert response_data_decoded == 'El monto total de la factura es de 199.65 €.'
    # Agrega más aserciones para validar la respuesta


""" def test_get_text_from_pdf_file():
    # Aquí puedes añadir la lógica para crear un archivo PDF de prueba o usar uno existente
    test_files = [
        '/home/southatoms/Escritorio/unitaryTest/unumIA/src/test/filesTest/Certificado Camara de Comercio  AIO 26 oct  2023.pdf']
    expected_output = "El documento está a nombre de AIO VIRTUAL S.A.S."
    print('RTA=', get_text_from_files(test_files))
    assert get_text_from_files(test_files) == expected_output


def test_get_text_from_image_file():
    # Similar a lo anterior, pero con un archivo de imagen
    test_files = [
        '/home/southatoms/Escritorio/unitaryTest/unumIA/src/test/filesTest/pruebaFactura.jpeg']
    expected_output = "El texto esperado que se extrae de la imagen"
    print('RTA=', get_text_from_files(test_files))
    assert get_text_from_files(test_files) == expected_output """

# Puedes añadir más pruebas para diferentes tipos de archivos y casos
