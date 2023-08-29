## Preguntale al Candidato

Usa inteligencia artificial basada en GPT-4 para hacerle pregunta a los candidatos presidenciales

### Detalles tecnicos
* Langchain / OpenAI
* Chroma (vector store)
* FastAPI
* NextJS

Se necesita python `>=3.9`. Para instalar las dependencias, crear un entorno virtual y ejecutar `pip install -r requirements.txt`

**No olvidarse de crear un archivo `.env` en el directorio root y agregar el token de OpenAI en la variable de entorno `OPENAI_API_KEY` en la forma `OPENAI_API_KEY=<token>`**

### Embeddings

Se generaron embeddings de las transcripciones usando OpenAI y Chroma como base de datos de vectores.
Chroma corre localmente con este proyecto, y la base de datos se encuentra en el directorio `db`

### Semantic cache

Se ha implementado un *semantic cache*, vectorizando las preguntas y guardando los embeddings usando chroma, en el directorio `cache_chroma`. De esta forma, para preguntas con significado semantico similar, no se llamara al LLM y se usara la respuesta cacheada, mejorando los tiempos de respuesta y optimizando costos de llamadas a la API de OpenAI.
Langchain actualmente no soporta semantic caching usando Chroma, por lo que en este proyecto hemos creado una nueva clase `ChromaSemanticCache` que implementa la interfas `BaseCache` de Langchain.

[Langchain QA docs](https://python.langchain.com/docs/use_cases/question_answering/)

![My Image](images/architectureCaching.png)


### Frontend

Ver repositorio [frontend](https://github.com/preguntale-al-candidato/frontend).

### Backend - FastAPI

Para correr el servidor ejecutar `uvicorn main:app --reload` \
Los endpoints de la api empiezan con `/api/` \
El frontend se sirve desde el root path `/`
