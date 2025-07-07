from typing import List
from interface.base_datastore import BaseDatastore, DataItem
import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.api.types import QueryResult
from chromadb.config import Settings


class Datastore(BaseDatastore):

    DB_COLLECTION_NAME = 'rag-table'

    def __init__(self):
        self.vector_db = chromadb.HttpClient(host='chromadb', port=8000, settings=Settings(allow_reset=True))
        self.collection : Collection = self.vector_db.get_or_create_collection(self.DB_COLLECTION_NAME)

    def reset(self) -> Collection:
        try:
            self.vector_db.delete_collection(self.DB_COLLECTION_NAME)
        except ValueError as e:
            print(f"Collection {self.DB_COLLECTION_NAME} does not exist. Creating a new one.")
        
        self.collection = self.vector_db.create_collection(self.DB_COLLECTION_NAME)
        print(f"✅ Collection Reset: {self.collection.count()} items in {self.DB_COLLECTION_NAME}")
        return self.collection

    def add_items(self, items: List[DataItem]) -> None:
        ids = []
        documents = []
        metadatas = []

        if items:
            for i, data in enumerate(items):
                ids.append(f"id{i+1}")
                documents.append(data.content)
                metadatas.append({"source": data.source})
            try:
                self.collection.add(ids=ids, documents=documents, metadatas=metadatas)
            except Exception as e:
                print(f"Error adding to db: {e}")
        else:
            print("add_items() failed: empty items array")

    def search(self, questions : List[str], top_k: int = 3) -> List[List[str]]:
        try:
            search_result : QueryResult = self.collection.query(
                query_texts=questions,
                n_results=top_k,
                include=["documents", "distances"]
            )

            result_content = []
            documents = search_result.get('documents', None)
            if documents is not None:
                for doc_list in documents:
                    result_content.append(doc_list)
            
                return result_content
            else:
                print("No docs found in search.")
        
        except Exception as e:
            print(f"Error during search(): {e}")
            
