from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class DataItem(BaseModel):
    content: str = ""
    source: str = ""


class BaseDatastore(ABC):
    @abstractmethod
    def add_items(self, items: List[DataItem]) -> None:
        pass

    @abstractmethod
    def search(self, questions : List[str], top_k: int = 3) -> List[List[str]]:
        pass