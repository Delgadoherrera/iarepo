import os
import pickle
from text_extraction import process_files
from text_processing import create_vector_store
from conversation_chain import create_conversation_chain, handle_user_input

# Función principal para ejecutar el flujo completo de procesamiento de texto y generación de respuesta


def main(question, files=None, pdf_url=None, base64_data=None, max_tokens=550, temperature=0.2, chunk_size=1000, chunk_overlap=200):
    raw_text = process_files(files, pdf_url, base64_data)
    if not raw_text:
        return "No hay texto disponible para procesar."

    vector_file_name = "vector_store.pkl"
    if os.path.exists(vector_file_name):
        with open(vector_file_name, 'rb') as f:
            vector_store = pickle.load(f)
    else:
        vector_store = create_vector_store(raw_text, chunk_size, chunk_overlap)
        with open(vector_file_name, 'wb') as f:
            pickle.dump(vector_store, f)

    conversation_chain = create_conversation_chain(
        vector_store, max_tokens, temperature)
    answer = handle_user_input(question, conversation_chain)

    if os.path.exists(vector_file_name):
        os.remove(vector_file_name)

    print('answerApi:', answer)

    return answer


# Punto de entrada principal cuando se ejecuta el script
if __name__ == "__main__":
    print(main())
