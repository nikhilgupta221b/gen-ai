from fastapi import FastAPI
from ollama import Client
from fastapi import Body

app = FastAPI()
client = Client(
  host='http://localhost:11434'
)

client.pull('gemma3:4b')

@app.post("/chat")
def chat(message: str = Body(..., description="Chat Message")):
    response = client.chat(model="gemma3:4b", messages=[
        { "role": "user", "content": message }
    ])

    return response['message']['content']