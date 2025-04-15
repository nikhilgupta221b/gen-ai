from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "Taj mahal is in india and it's white in colour. It's in agra city of Uttar Pradesh"

response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)

print("Vector Embeddings: ", response.data[0].embedding)