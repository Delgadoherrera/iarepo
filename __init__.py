import os
from flask import Flask, request, jsonify
from main import main
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')
FLASK_DEBUG = os.getenv('FLASK_DEBUG')

@app.route("/")
def hello_world():
    return jsonify(statusCode="200",statusMessage="OK")

@app.route('/ia/api/assets/answer', methods=['POST'])
def get_answer():
    question = request.form.get('question')
    uploaded_file = request.files.get('file')
    base64_image = request.form.get('base64_image')
    pdf_url = request.form.get('url')
    if not question:
        return jsonify({'error': 'La pregunta es requerida'}), 400

    files = []
    temp_file = None
    base64_data = None

    if uploaded_file:
        temp_file = os.path.join('/tmp', uploaded_file.filename)
        uploaded_file.save(temp_file)
        files = [temp_file]
    elif base64_image:
        base64_data = base64_image
    elif pdf_url:
        # Manejo adicional para pdf_url si es necesario
        pass
    else:
        return jsonify({'error': 'Se requiere un archivo, datos base64 o URL'}), 400

    try:
        answer = main(question, files, pdf_url, base64_data)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error en el procesamiento'}), 500

    # Limpieza de archivo temporal
    if temp_file:
        os.remove(temp_file)

    return answer


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, port=FLASK_RUN_PORT)
