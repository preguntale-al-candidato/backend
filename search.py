from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from prompts import get_assistant_prompt_spanish
from prompts import get_assistant_prompt_spanis_one_shot
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from cache.milvus import MilvusSemanticCache
import langchain
from langchain.llms import OpenAI
from typing import List
from langchain.vectorstores import Milvus
from config import get_milvus_connection

import os


class Search():

    FILTER_THRESHOLD = 0.40
    MAX_RESULTS_SIMILARITY_SEARCH = 10

    # TODO - to be defined how to determine the collection name based on the candidate
    COLLECTION_NAME = "milei"

    def __init__(self) -> None:
        load_dotenv()
        embedding = OpenAIEmbeddings()
        self.vectordb = Milvus(embedding_function=embedding,
                               connection_args=get_milvus_connection(), collection_name=self.COLLECTION_NAME)
        langchain.llm_cache = MilvusSemanticCache(
            embedding=OpenAIEmbeddings(), score_threshold=0.15)

    def search(self, query: str = None):
        results = self.vectordb.similarity_search_with_score(
            query, k=self.MAX_RESULTS_SIMILARITY_SEARCH)
        filtered_results = [
            r for r in results if r[1] <= self.FILTER_THRESHOLD]
        docs = list(map(lambda result: result[0], filtered_results))
        print("Nelson")
        print(docs)
        if (os.environ.get("USE_DIARIZED_DB") == "true"):
            print("Using diarized db")
            prompt = get_assistant_prompt_spanis_one_shot()
        else:
            print("Using non-diarized db")
            prompt = get_assistant_prompt_spanish()

        if (len(docs) == 0):
            print("No sources found")
            return {"answer": "No se encontraron resultados", "sources": []}

        # llm = ChatOpenAI(model_name="gpt-4", temperature=1) # TODO - haven' figured out yet how to use a chat model with the semantic cache.
        llm = OpenAI(model_name="gpt-4", temperature=1)
        chain = load_qa_chain(llm, chain_type="stuff",
                              prompt=prompt, verbose=False)
        answer = chain(
            {"input_documents": docs, "question": query}, return_only_outputs=True)
        return self.build_response(answer, docs)

    def build_response(self, answer, docs):
        if not "output_text" in answer:
            return {"answer": "No se encontraron resultados", "sources": []}
        answer = answer.get("output_text")
        return {"answer": answer, "sources": self.build_sources(docs)}

    def build_sources(self, docs) -> List:
        sources = []
        for doc in docs:
            metadata = doc.metadata
            if metadata is not None:
                link = metadata.get("link") + "&t=" + \
                    str(int(metadata.get("start")))
                source = {"name": metadata.get(
                    "name"), "link": link, "text": doc.page_content, "time": int(metadata.get("start"))}
                sources.append(source)
        return sources
