## Preguntale al Candidato - Backend

Usa inteligencia artificial basada en GPT-3.5-Turbo para hacerle pregunta a los candidatos presidenciales.

Herramientas utilizadas
* Langchain / OpenAI
* Milvus (vector store)
* FastAPI

Se necesita python `>=3.9`. Para instalar las dependencias, crear un entorno virtual y ejecutar `pip install -r requirements.txt`

**No olvidarse de crear un archivo `.env` en el directorio root y agregar el token de OpenAI en la variable de entorno `OPENAI_API_KEY` en la forma `OPENAI_API_KEY=<token>`**

## Embeddings

Se generaron embeddings de las transcripciones usando OpenAI y Milvus como base de datos de vectores.

Para correr Milvus localmente ver el repositorio [db](https://github.com/preguntale-al-candidato/db).

## Semantic cache

Se ha implementado un *semantic cache*, vectorizando las preguntas y guardando los embeddings en una colleccion en Milvus. De esta forma, para preguntas con significado semantico similar, no se llamara al LLM y se usara la respuesta cacheada, mejorando los tiempos de respuesta y optimizando costos de llamadas a la API de OpenAI.
Langchain actualmente no soporta semantic caching usando Milvus, por lo que en este proyecto hemos creado una nueva clase `MilvusSemanticCache` que implementa la interfas `BaseCache` de Langchain.

[Langchain QA docs](https://python.langchain.com/docs/use_cases/question_answering/)

![My Image](images/architectureCaching.png)

## Backend - FastAPI

### How to run

Pasos para correr el servidor localmente:

1. Vea el repositorio [preguntale-al-candidato/db](https://github.com/preguntale-al-candidato/db) para correr la base de datos Milvus.

2. Generar un entorno virtual

```bash
pip install virtualenv
virtualenv env
```

3. Activar el entorno virtual

```bash
source env/bin/activate  // En Unix (Linux y MacOS)
env/Scripts/activate.bat // En Windows (CMD)
env/Scripts/Activate.ps1 // En WIndows (Powershell)
```

4. Instalar las dependencias

```bash
pip install --upgrade pip
pip install --requirement requirements.txt
```

5. (Opcional) Ingesta de transcripciones.

Si la base de datos levantada en el paso `1` fue creada desde un backup en S3 **OMITA** este paso.

```bash
cd ingestion
mkdir -p processed_transcriptions
python save_embedings.py
```

6. Correr el servidor ejecutando:

```bash
uvicorn main:app --reload
```
Los endpoints de la api empiezan con `/api/` \

7. Correr el frontend

Una vez que el backend esta listo, a partir del repositorio [preguntale-al-candidato/frontend](https://github.com/preguntale-al-candidato/frontend) podrá correr el frontend y acceder a la interfaz gráfica.
