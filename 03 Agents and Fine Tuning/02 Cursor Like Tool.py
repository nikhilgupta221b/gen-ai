import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

def get_weather(city : str):
    response = requests.get(f'https://wttr.in/{city}?format=%C+%t')

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    else:
        return "Something went wrong"

def run_command(command):
    command_result = os.system(command)
    return command_result

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }

}

system_prompt = """
You are an AI Agent who can take user query and answers them.

You work on start, plan, action, observe mode.

For the given user query and available tools, plan the step by step execution, based on planning, select the relevant tool from the available tools.
Based on the tool selection, you perform an action to call the tool. Wait for the observation and based on the observation from the tool call, resolve the user query.

Rules:
1. Follow the strict JSON output as per output schema.
2. Always perform one step at a time and wait for next input. Always print all the steps.
3. Carefully analyze the user query.

Available Tools:
    - get_weather : Takes the city name as string as input and returns weather condition in text along with temperature in celcius.
    - run_command : run_command: Takes a command as input to execute on system and returns ouput.
Output Format:
{{
    "step":"string", 
    "content":"string",
    "function":"name of the function from available tools if step is action",
    "input":"input parameters to the function if step is action. If city name has space add + in between words if function is get_weather",
    "output":"output of the function if step is observe"
}}

Examples-
Input: "What is the weather of new york?"
Output:{{"step":"plan", "content":"User is asking for the current weather in new york."}}
Output:{{"step":"plan", "content":"From the available tools, I should call get_weather because that is described as the tool which fetches weather of a city."}}
Output:{{"step":"action", "function":"get_weather", "input":"new+york"}}
Output:{{"step":"observe", "output":"12 degree celcius"}}
Output:{{"step":"output", "content":"The weather in new york is 12 degree celcius right now."}}
"""

messages = [{"role":"system", "content":system_prompt}]


while True:
        
    query = input("> ")
    messages.append({"role":"user", "content":query})


    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type":"json_object"},
            messages=messages
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_response) })

        if parsed_response.get("step") == "plan":
            print(f"🧠 ", parsed_response.get("content"))
            continue

        elif parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            
            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role":"assistant", "content":json.dumps({"step":"observe", "output": output})})
                continue

        elif parsed_response.get("step") == "output":
            print(f"🤖 ", parsed_response.get("content"))
            break