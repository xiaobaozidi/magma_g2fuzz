from openai import OpenAI
import os

with open('openai_key.txt', 'r') as file:
    key = file.read().strip()

OPENAI_KEY = key

def llm(model, prompt, temperature):
    client = OpenAI(api_key=OPENAI_KEY)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content

def llm_messages(model, messages, temperature):
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = """
    hi
    """
    print(llm("gpt-4o-mini-2024-07-18", prompt))