import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "HuggingFaceH4/starchat-beta"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16,
    device_map="cuda"
)

print("Model loaded successfully")

prompt = "Write a Python function that adds two numbers."

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

print("Generating output...")

outputs = model.generate(
    **inputs,
    max_new_tokens=50
)

print("\nGenerated Text:\n")
print(tokenizer.decode(outputs[0]))