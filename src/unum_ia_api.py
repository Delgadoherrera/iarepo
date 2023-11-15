import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from main import main
load_dotenv()

app = Flask(__name__)

FLASK_RUN_PORT = os.getenv('FLASK_RUN_PORT')

print('PORT', FLASK_RUN_PORT)


@app.route('/ia/api/assets/answer', methods=['POST'])
def get_answer():
    question = request.form.get('question')
    uploaded_file = request.files.get('file')
    base64_image = request.form.get('base64_image')
    pdf_url = request.form.get('url')
    max_tokens = request.form.get('max_tokens', default=550, type=int)
    temperature = request.form.get('temperature', default=0.2, type=float)
    chunk_size = request.form.get('chunk_size', default=1000, type=int)
    chunk_overlap = request.form.get('chunk_overlap', default=200, type=int)

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
        answer = main(question, files, pdf_url, base64_data, max_tokens, temperature, chunk_size, chunk_overlap)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error en el procesamiento'}), 500

    # Limpieza de archivo temporal
    if temp_file:
        os.remove(temp_file)

    return answer


if __name__ == '__main__':
    app.run(debug=True, port=FLASK_RUN_PORT)
