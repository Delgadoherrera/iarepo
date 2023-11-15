from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import openai

# Función para crear una cadena de conversación con un modelo de lenguaje y un almacén de vectores
def create_conversation_chain(vector_store):
    llm = ChatOpenAI(model="gpt-4", openai_api_key=openai.api_key, max_tokens=550, temperature=0.2)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)

# Función para manejar la entrada del usuario y obtener una respuesta del modelo de lenguaje
def handle_user_input(question, conversation_chain):
    try:
        response = conversation_chain({'question': question})
        return response['chat_history'][-1].content
    except Exception as ex:
        print('Error al manejar la entrada del usuario:', ex)
        return None
