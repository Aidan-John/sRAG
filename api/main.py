import glob
import json
import os
from typing import List
from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator, Evaluator
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_SOURCE_PATH = os.path.join("dataset", "eval", "eval_data")
DEFAULT_EVAL_PATH = os.path.join("dataset", "eval", "eval_questions", "sample_questions.json")

def create_pipeline() -> RAGPipeline:
    """Create and return a new RAG Pipeline instance with all components."""
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    evaluator = Evaluator()
    return RAGPipeline(datastore, indexer, retriever, response_generator, evaluator)


def get_files_in_directory(source_path: str) -> List[str]:
    if os.path.isfile(source_path):
        return [source_path]
    return glob.glob(os.path.join(source_path, "*"))

pipeline = create_pipeline()
source_path = DEFAULT_SOURCE_PATH
eval_path = DEFAULT_EVAL_PATH
document_paths = get_files_in_directory(source_path)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/reset")
def reset_db():
    print("🗑️  Resetting the database...")
    pipeline.reset()
    return {"response": "Database reset successful."}

@app.post("/add_documents")
def add_documents():
    print("📥  Adding documents...")
    pipeline.add_documents(document_paths)
    return {"response": "Documents added successfully."}

@app.post("/evaluate")
def evaluate(background_tasks: BackgroundTasks):
    print(f"📝  Evaluating questions from {eval_path}")
    with open(eval_path, "r") as f:
        questions = json.load(f)
    background_tasks.add_task(pipeline.evaluate, questions)
    return {"response": "Evaluation in progress. Check API logs for results."}

@app.post("/query")
def query(q: str):
    print("🔍  Processing query...")
    response = pipeline.process_query(query=q, search_results=None)
    return {"response": response}

