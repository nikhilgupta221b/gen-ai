import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant who helps users to solve their queries by breaking down the problems into steps and then finally providing and output.

For any user input you have to think before you answer. You have to think in 5-6 steps atleast and then give the output.

Follow these steps in the sequence for an input, analyze, think, output, valdiate, result.

The steps are you get a user input, you analyze, you think, you again think for several times, then return output with explaination and then you validate the output before giving final result.

Rules:
1. Follow the strict JSON output as per output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyze the user query.

Output Format:
{{step:"string", "content":"string"}}

Examples-
Input: "What is 2 + 2?"
Output:{{step:"analyze", content:"The user has asked to solve a maths question which is an arithmatic operation of addition."}}
Output:{{step:"think", content:"To perform addition, I should go from left to right and add all operands."}}
Output:{{step:"output", content:"The output is 4."}}
Output:{{step:"validate", content:"The output 4 is indeed correct as 2 + 2 is 4."}}
Output:{{step:"result", content:"2+2 is 4. This is the addition operation which results in addition of two numbers."}}
"""

messages = [{"role":"system", "content":system_prompt}]

query = input("> ")
messages.append({"role":"user", "content":query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"json_object"},
        messages=messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant", "content":json.dumps(parsed_response)})

    if parsed_response.get("step") != "output":
        print(f"🧠 ", parsed_response.get("content"))
        continue
    else:
        print(f"🤖 ", parsed_response.get("content"))
        break