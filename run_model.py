import os
from openai import OpenAI


BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.2:1b"

model = OpenAI(base_url=BASE_URL, api_key="ollama")

def ask_llm(prompt):
    system_prompt = "You are a helpful assistant"
    messages = [{"role":"system", "content":system_prompt}, {"role":"user", "content": prompt}]
    response = model.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content
