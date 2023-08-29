import time
import json
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
from typing import List

load_dotenv()

TRANSCRIPTIONS_PATH = "transcriptions"
PROCESSED_TRANSCRIPTIONS_FILENAME = "processed_transcriptions.json"
SPEAKER_MAX_ACCEPTABLE_DISTANCE = 0.5

def to_chunks(name, link, transcription_path, chunk_length=1000):
    try:
        with open(transcription_path, 'r') as f:
            transcript = json.loads(f.read())
        start = None
        chunks = []
        metadatas = []
        chunk = ""
        for item in transcript:
            if(item['identity_distance'] >= SPEAKER_MAX_ACCEPTABLE_DISTANCE):
                # It's probably not the speaker we are interested in, so skip it
                print("Skipping line as it's not desired speaker")
                continue
            if start is None:
                start = item['start']
            if(len(item['text']) > chunk_length):
                item['text'] = item['text'][:chunk_length - 100]
            temp_chunk = chunk + " " + item['text'] + " "
            if(len(temp_chunk) <= chunk_length):
                chunk = temp_chunk
            else:
                chunks.append(chunk)
                metadata = {'name': name, 'link': link, 'start': start}
                metadatas.append(metadata)
                start = item['start']
                chunk = item['text']

        return chunks, metadatas
    except Exception as e:
        print("Error reading transcription", e)
        return [], []

def save_embedings(persist_directory: str = "db", chunks: list = None, metadatas: list = None):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(chunks, embeddings, metadatas=metadatas, persist_directory=persist_directory)

def save_updated_episodes(episodes: List, filename: str = PROCESSED_TRANSCRIPTIONS_FILENAME):
    with open(filename, 'w') as f:
        f.write(json.dumps(episodes))

def build_url(id):
    return "https://www.youtube.com/watch?v=" + id


def main():
    print("Starting")
    persist_directory = "../db"
    with open(PROCESSED_TRANSCRIPTIONS_FILENAME, 'r') as f:
        processed_transcriptions: List = json.load(f)
        
        file_list = os.listdir(TRANSCRIPTIONS_PATH)
        for file_name in file_list:
            if(file_name in processed_transcriptions):
                print("Skipping as already processed, title: ", file_name)
                continue
            file_path = TRANSCRIPTIONS_PATH + "/" + file_name
            url = build_url(file_name)
            title = "test title"
            print("Processing", title)
            chunks, metadatas = to_chunks(title, url, file_path)
            if(len(chunks) == 0 or len(metadatas) == 0):
                print("No chunks to process due to an exception for", title)
                continue
            try:
                save_embedings(persist_directory, chunks, metadatas)
                processed_transcriptions.append(file_name)
                save_updated_episodes(processed_transcriptions)
                time.sleep(1)
            except Exception as e:
                print("Error saving embedings", e)
                continue

if __name__ == "__main__":
    main()