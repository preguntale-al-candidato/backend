import time
import json
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Milvus
from dotenv import load_dotenv
from typing import List

load_dotenv()

# TODO - to be defined how to determine
TRANSCRIPTIONS_PATH = "transcriptions"
PROCESSED_TRANSCRIPTIONS_PATH = "processed_transcriptions"
SPEAKER_MAX_ACCEPTABLE_DISTANCE = 0.5


def to_chunks(candidate: str, transcription_path, chunk_length=1000):
    try:
        with open(transcription_path, 'r') as f:
            transcript = json.loads(f.read())
        start = None
        chunks = []
        metadatas = []
        chunk = ""
        segments = transcript['segments']
        name = transcript['title']
        link = transcript['url']
        print(f"Processing {len(segments)} segments")
        for item in segments:
            if (item['is_candidate']) is False:
                continue
            if start is None:
                start = item['start']
            if (len(item['text']) > chunk_length):
                item['text'] = item['text'][:chunk_length - 100]
            temp_chunk = chunk + " " + item['text'] + " "
            if (len(temp_chunk) <= chunk_length):
                chunk = temp_chunk
            else:
                chunks.append(f"{candidate} dijo: {chunk}")
                metadata = {'name': name, 'link': link, 'start': start}
                metadatas.append(metadata)
                start = item['start']
                chunk = item['text']

        return chunks, metadatas
    except Exception as e:
        print("Error reading transcription", e)
        return [], []


def save_embedings(collection_name: str, chunks: list = None, metadatas: list = None):
    embeddings = OpenAIEmbeddings()
    print(f"Saving {len(chunks)} chunks in database")
    milvus_host = os.getenv("MILVUS_HOST", default="localhost")
    milvus_port = os.getenv("MILVUS_PORT", default="19530")
    vectordb = Milvus.from_texts(
        chunks, embeddings, metadatas=metadatas, collection_name=collection_name,
        connection_args={"host": milvus_host, "port": milvus_port})


def save_updated_episodes(file_path: str, episodes: List):
    with open(file_path, 'w') as f:
        f.write(json.dumps(episodes))


def build_url(id):
    return "https://www.youtube.com/watch?v=" + id


def main():
    print("Starting")
    candidate_dirs = os.listdir(TRANSCRIPTIONS_PATH)
    for candidate in candidate_dirs:
        candidate_path = TRANSCRIPTIONS_PATH + "/" + candidate
        file_list = os.listdir(candidate_path)
        processed_transcriptions_path = PROCESSED_TRANSCRIPTIONS_PATH + \
            "/" + candidate + ".json"

        try:
            with open(processed_transcriptions_path, 'r') as f:
                processed_transcriptions: List = json.load(f)
        except:
            with open(processed_transcriptions_path, "w") as file:
                file.write(json.dumps([]))
                processed_transcriptions: List = []

        transcriptions_fully_processed = 0
        for file_name in file_list:
            if (file_name in processed_transcriptions):
                print("Skipping as already processed, title: ", file_name)
                continue
            file_path = candidate_path + "/" + file_name
            chunks, metadatas = to_chunks(candidate, file_path)
            if (len(chunks) == 0 or len(metadatas) == 0):
                print("No chunks to process due to an exception for", file_name)
                continue
            try:
                save_embedings(candidate, chunks, metadatas)
                processed_transcriptions.append(file_name)
                save_updated_episodes(
                    processed_transcriptions_path, processed_transcriptions)
                time.sleep(1)
                transcriptions_fully_processed = transcriptions_fully_processed + 1
            except Exception as e:
                print("Error saving embedings", e)
                continue

        print(
            f"Finished processing {transcriptions_fully_processed} episodes for candidate {candidate}")


if __name__ == "__main__":
    main()
