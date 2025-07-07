from interface.base_datastore import BaseDatastore
from interface.base_retriever import BaseRetriever
from typing import List


class Retriever(BaseRetriever):
    def __init__(self, datastore: BaseDatastore):
        self.datastore = datastore

    def search(self, query_vectors: List[List[float]], top_k: int = 3) -> list[str]:
        search_results = self.datastore.search(query_vectors, top_k=top_k)
        return search_results