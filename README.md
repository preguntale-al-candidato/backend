## Preguntale al Candidato

Usa inteligencia artificial basada en GPT-4 para hacerle pregunta a los candidatos presidenciales

### Detalles tecnicos
* Langchain / OpenAI
* Milvus (vector store)
* FastAPI
* NextJS

Se necesita python `>=3.9`. Para instalar las dependencias, crear un entorno virtual y ejecutar `pip install -r requirements.txt`

**No olvidarse de crear un archivo `.env` en el directorio root y agregar el token de OpenAI en la variable de entorno `OPENAI_API_KEY` en la forma `OPENAI_API_KEY=<token>`**

### Embeddings

Se generaron embeddings de las transcripciones usando OpenAI y Milvus como base de datos de vectores.
Para correr Milvus en docker, correr 
```
docker compose up -d
```
en el root directory donde se encuentra el archivo `docker-compose.yml`

### Semantic cache

Se ha implementado un *semantic cache*, vectorizando las preguntas y guardando los embeddings en una colleccion en Milvus. De esta forma, para preguntas con significado semantico similar, no se llamara al LLM y se usara la respuesta cacheada, mejorando los tiempos de respuesta y optimizando costos de llamadas a la API de OpenAI.
Langchain actualmente no soporta semantic caching usando Milvus, por lo que en este proyecto hemos creado una nueva clase `MilvusSemanticCache` que implementa la interfas `BaseCache` de Langchain.

[Langchain QA docs](https://python.langchain.com/docs/use_cases/question_answering/)

![My Image](images/architectureCaching.png)


### Frontend - NextJS
El frontend se ha hecho de una manera estatica, hay que generar el html de antemano para que sea servido por FastAPI. Hay que ejecutar el siguiente comando `npm run build` cada vez que se hace un cambio en el frontend. El repo contiene la version estatica del frontend por lo que no es necesario ejecutar este comando cuando se clona el proyecto.


### Backend - FastAPI

Para correr el servidor ejecutar `uvicorn main:app --reload` \
Los endpoints de la api empiezan con `/api/` \
El frontend se sirve desde el root path `/`
