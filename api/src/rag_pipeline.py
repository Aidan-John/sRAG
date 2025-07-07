from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Dict, List, Optional
from interface import (
    BaseDatastore,
    BaseIndexer,
    BaseRetriever,
    BaseResponseGenerator,
    BaseEvaluator,
    EvaluationResult,
)


@dataclass
class RAGPipeline:
    """Main RAG pipeline that orchestrates all components."""

    datastore: BaseDatastore
    indexer: BaseIndexer
    retriever: BaseRetriever
    response_generator: BaseResponseGenerator
    evaluator: Optional[BaseEvaluator] = None

    def reset(self) -> None:
        """Reset the datastore."""
        self.datastore.reset()

    def add_documents(self, documents: List[str]) -> None:
        """Index a list of documents."""
        items = self.indexer.index(documents)
        self.datastore.add_items(items)
        print(f"✅ Added {len(items)} items to the datastore.")

    def process_query(self, query: str, search_results : List[str]) -> str:
        """Process a query by searching the datastore if context not provided and generating a response."""
        if search_results is None:
            search_results = list(map(''.join, self.datastore.search([query])))

        for i, result in enumerate(search_results):
            print(f"🔍 Result {i+1}: {result}\n")

        response = self.response_generator.generate_response(query, search_results)
        return response

    def evaluate(
        self, sample_questions: List[Dict[str, str]]
    ) -> None:
        """Evaluate the RAG pipeline using a set of sample questions."""
        questions = [item["question"] for item in sample_questions]
        expected_answers = [item["answer"] for item in sample_questions]
        context = self.datastore.search(questions)

        for i in range(len(questions)):
            print(f"✅ Found {len(context[i])} results for query: {i + 1}\n")
            print(f"Q {i+1}: {questions[i]}")
            print(f"Expected Answer: {expected_answers[i]}")
            for idx, result in enumerate(context[i]):
                print(f"🔍 Result {idx+1}: {result}\n")

        with ThreadPoolExecutor(max_workers=2) as executor:
            results: List[EvaluationResult] = list(
                executor.map(
                    self._evaluate_single_question,
                    questions,
                    expected_answers,
                    context,
                )
            )

        for i, result in enumerate(results):
            result_emoji = "✅" if result.is_correct else "❌"
            print(f"{result_emoji} Q {i+1}: {result.question}: \n", flush=True)
            print(f"Response: {result.response}\n", flush=True)
            print(f"Expected Answer: {result.expected_answer}\n", flush=True)
            print(f"Reasoning: {result.reasoning}\n", flush=True)
            print("--------------------------------", flush=True)

        number_correct = sum(result.is_correct for result in results)
        print(f"✨ Total Score: {number_correct}/{len(results)}", flush=True)

    def _evaluate_single_question(self, question: str, expected_answer: str, context: List[str]) -> EvaluationResult:
        
        response = self.process_query(question, context)
        result = self.evaluator.evaluate(question, response, expected_answer)
        return result