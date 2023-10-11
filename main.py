from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from search import Search

services = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Load models...")
    services["search"] = Search()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3001",
    "https://preguntalealcandidato.com",
    "https://api.preguntalealcandidato.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=501)
async def root():
    return {"message": "Not implemented"}


@app.head("/health", status_code=200)
@app.get("/health", status_code=200)
async def health():
    return {"message": "status: OK"}


@app.get("/api/ping")
async def hello():
    return {"message": "pong"}


@app.get("/api/test")
async def test(query: str = None):
    return {"response": query}


@app.get("/api/search")
async def search(candidate: str = None, query: str = None):
    supported_candidates = ["bregman", "bullrich", "massa", "milei", "schiaretti"]
    if (candidate is None or candidate not in supported_candidates):
        print("Candidate is None or is not a supported name")
        return {"answer": "El candidato ingresado no es válido", "sources": []}

    search = services["search"]
    # validate search has been loaded
    if search is None:
        raise HTTPException(status_code=500, detail="Search module not found")
    response = search.search(candidate_name=candidate, query=query)
    return {"response": response}
