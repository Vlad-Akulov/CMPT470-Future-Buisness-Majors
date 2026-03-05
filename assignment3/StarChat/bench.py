import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datasets import load_dataset
import random

MODEL_NAME = "HuggingFaceH4/starchat-beta"
NUM_PAIRS = 300

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading StarChat 16B model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    dtype=torch.float16
)

model.eval()

def build_prompt(code1, code2):
    prompt = f"""
You are a software clone detection tool.

Determine if the following two Java functions implement the same functionality.

Respond ONLY with:
YES
or
NO

Function A:
{code1}

Function B:
{code2}

Answer:
"""
    return prompt


def predict_clone(code1, code2):

    prompt = build_prompt(code1, code2)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=5,
            temperature=0.0
        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)

    response = response.split("Answer:")[-1].strip().upper()

    if "YES" in response:
        return 1
    else:
        return 0

print("[INFO] Loading BigCloneBench dataset from HuggingFace...")

dataset = load_dataset(
    "google/code_x_glue_cc_clone_detection_big_clone_bench",
    split="test"
)

print(f"[INFO] Dataset loaded: {len(dataset)} total examples")

# randomly sample the pairs we want to test
indices = random.sample(range(len(dataset)), NUM_PAIRS)
data_subset = [dataset[i] for i in indices]

print(f"[INFO] Sampled {NUM_PAIRS} examples for benchmarking")

y_true = []
y_pred = []

print("Running benchmark...")

for example in tqdm(data_subset, total=len(data_subset)):

    code1 = example["func1"]
    code2 = example["func2"]
    label = example["label"]

    pred = predict_clone(code1, code2)

    y_true.append(label)
    y_pred.append(pred)

print("\nBenchmark Results")

acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("Accuracy :", acc)
print("Precision:", prec)
print("Recall   :", rec)
print("F1 Score :", f1)