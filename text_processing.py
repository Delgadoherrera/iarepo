from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import openai

# Función para crear un almacén de vectores (vector store) a partir de texto
def create_vector_store(raw_text):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    text_chunks = text_splitter.split_text(raw_text)
    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    return FAISS.from_texts(text_chunks, embeddings)
