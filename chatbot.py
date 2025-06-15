from transformers import AutoTokenizer, BitsAndBytesConfig, Gemma3ForCausalLM
import torch
from huggingface_hub import login
from transformers import pipeline
import torch

pipe = pipeline("text-generation", model="google/gemma-3-1b-it", device_map="auto", torch_dtype=torch.bfloat16)

messages = [
    [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."},]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "Write a poem on Hugging Face, the company"},]
        },
    ],
]

output = pipe(messages, max_new_tokens=50)
print(output[0][0]['generated_text'][-1]["content"])
