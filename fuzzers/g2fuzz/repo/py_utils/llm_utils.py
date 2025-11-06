from openai import OpenAI
import os
from enum import Enum

class LLMModel(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_4 = "gpt-4"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_O = "gpt-4o"
    GPT_4_O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"
    GPT_4_5 = "gpt-4.5"
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_NANO = "gpt-5-nano"
    O1 = "o1"
    O1_MINI = "o1-mini"
    O1_PRO = "o1-pro"
    O3 = "o3"
    O3_MINI = "o3-mini"
    O3_PRO = "o3-pro"
    O4_MINI = "o4-mini"

with open('openai_key.txt', 'r') as file:
    key = file.read().strip()

OPENAI_KEY = key

def llm(model, prompt, temperature=1):
    # Validate model is a valid OpenAI model
    valid_models = {m.value for m in LLMModel}
    if model not in valid_models:
        raise ValueError(f"Invalid model: {model}. Must be one of: {', '.join(valid_models)}")
    
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1
    )

    return response.choices[0].message.content

def llm_messages(model, messages, temperature=1):
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = """
    hi
    """
    print(llm("gpt-5-mini", prompt))