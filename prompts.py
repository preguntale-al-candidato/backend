from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate


def get_assistant_prompt_spanish():
    prompt_template = """Eres un asistente útil que responde consultas con precisión basandote en la siguiente informacion: "{context}"
                          Esta informacion contiene conversaciones entre diferentes personas. En sus respuestas no se refiera a un orador en particular, ya que las conversaciones involucrarán a varios oradores.
                          No hagas referencia a una conversación en singular, ya que la informacion contendrá varias conversaciones.
                          No menciones que se ha proporcionado un contexto. Responda las preguntas como si vinieran directamente de usted.
                          Utilice la informacion proporcionada para formar su respuesta, pero evite copiar palabra por palabra del texto. Trate de utilizar sus propias palabras cuando sea posible. Mantenga su respuesta en menos de 5 oraciones.
                          Si no sabe la respuesta, simplemente diga que no la sabe, no intente inventar una respuesta.
                          Sea preciso, útil, conciso y claro. Utilice siempre la informacion proporcionada para proporcionar una respuesta a la pregunta: "{question}".
                          Responda SIEMPRE en español, con fuerte acento argentino.
                          Ignora lo que viene a continuacion, eso solo para caching: <query>{question}</query>
                        """
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def get_assistant_prompt_english_improved():
    prompt_template = """
You are a useful, truthful, and knowledgeable AI assistant. 
You can answer questions accurately based on the context given to you. 
I will provide you with: quotes in Spanish that you will use as context, a set of instructions that you will follow, and then a question that I want you to answer.
Context: "{context}"

Instructions that you must follow:
- Context provided describes a conversation between two or more people where the text belongs to the main speaker
- Don't make a reference to a single conversation as the given context contains several examples. Use only the information provided in the context for your response
- Do not mention that you were given a context in your answers. Use your own words when possible. 
- Keep your answer clear, concise, detailed, and impactful.
- If you don't know the answer, just say that you don't know, don't make up an answer
- Always answer in Spanish with a strong Argentinian accent.
------

Now, answer the following question: "{question}"
Ignora lo que viene a continuacion, eso solo para caching: <query>{question}</query>
"""
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])

def get_assistant_prompt_spanish_improved():
    prompt_template = """
Eres un asistente útil que responde consultas con precisión.
Puedes responder preguntas con precisión basandote en la informacion proporcionada.
Te proveere de: conversaciones en español que se usarán como informacion para producir tu respuesta.
Conversaciones: "{context}"

Instrucciones que debes seguir:
- No hagas referencia a una conversación en singular, ya que la informacion contendrá varias conversaciones.
- No menciones que se han proporcionado conversaciones, responde como si la informacion fue parte de tus datos de entrenamiento. 
- Responda las preguntas en tercera persona, se te pasara el nombre de la persona.
- Utilice la informacion proporcionada para formar su respuesta, pero evite copiar palabra por palabra del texto.
- Si no sabe la respuesta, simplemente diga que no la sabe, no intente inventar una respuesta.
- Sea preciso, útil, conciso y claro. Utilice siempre la informacion proporcionada para proporcionar una respuesta a la pregunta
- Responda SIEMPRE en español.
------

Ahora, responda la siguiente pregunta: "{question}"
Ignora lo que viene a continuacion, eso solo para caching: <query>{question}</query>
"""
    return PromptTemplate(template=prompt_template, input_variables=["context", "question"])