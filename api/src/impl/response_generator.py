from typing import List
from interface.base_response_generator import BaseResponseGenerator
from util.invoke_ai import invoke_ai


SYSTEM_PROMPT = """Use the provided context to provide a concise answer to the user's question. If you cannot find the answer in the context, say so. Do not make up information."""


class ResponseGenerator(BaseResponseGenerator):
    def generate_response(self, query: str, context: List[str]) -> str:
        
        # Combine context into a single string
        context_text = "\n".join(context)
        user_message = (
            f"Instructions:\n{SYSTEM_PROMPT}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Question:\n{query}\n"
        )

        return invoke_ai(prompt=user_message)