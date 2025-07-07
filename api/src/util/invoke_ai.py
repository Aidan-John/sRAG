from ollama import Client, ChatResponse

def invoke_ai(prompt : str) -> str:
    
    client = Client(host="http://ollama:11434")
    response: ChatResponse = client.chat(
        model="gemma3:4b-it-qat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=False,
    )

    return response.message.content