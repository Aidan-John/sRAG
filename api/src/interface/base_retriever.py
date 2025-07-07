from abc import ABC, abstractmethod
from typing import List


class BaseRetriever(ABC):

    @abstractmethod
    def search(self, query_vectors: List[List[float]], top_k: int = 3) -> List[str]:
        pass