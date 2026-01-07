from openai import OpenAI
import os
from enum import Enum

class LLMModel(Enum):
    # OpenAI models
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
    # Claude models
    CLAUDE_SONNET_4_5 = "claude-sonnet-4-5"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-latest"
    CLAUDE_3_5_HAIKU = "claude-3-5-haiku-latest"
    CLAUDE_OPUS_4 = "claude-opus-4"

# Load API keys
try:
    with open('openai_key.txt', 'r') as file:
        OPENAI_KEY = file.read().strip()
except FileNotFoundError:
    OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

try:
    with open('anthropic_key.txt', 'r') as file:
        ANTHROPIC_KEY = file.read().strip()
except FileNotFoundError:
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")

def _is_claude_model(model):
    """Check if the model is a Claude model."""
    claude_models = {m.value for m in LLMModel if m.name.startswith("CLAUDE")}
    return model in claude_models

def llm(model, prompt, temperature=1):
    """Send a single prompt to the LLM."""
    valid_models = {m.value for m in LLMModel}
    if model not in valid_models:
        raise ValueError(f"Invalid model: {model}. Must be one of: {', '.join(valid_models)}")
    
    if _is_claude_model(model):
        from anthropic import Anthropic
        client = Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.content[0].text
    else:
        client = OpenAI(api_key=OPENAI_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content

def llm_messages(model, messages, temperature=1):
    """Send a conversation with multiple messages to the LLM."""
    if _is_claude_model(model):
        from anthropic import Anthropic
        client = Anthropic(api_key=ANTHROPIC_KEY)
        
        # Separate system message from other messages (Claude API requirement)
        system_msg = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                user_messages.append(msg)
        
        # Create API call parameters
        api_params = {
            "model": model,
            "max_tokens": 4096,
            "messages": user_messages,
            "temperature": temperature
        }
        if system_msg:
            api_params["system"] = system_msg
        
        response = client.messages.create(**api_params)
        return response.content[0].text
    else:
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
    print("Testing OpenAI...")
    print(llm("gpt-5-mini", prompt))
    print("--------------------------------")
    print("Testing Claude...")
    print(llm("claude-3-5-haiku-latest", prompt))