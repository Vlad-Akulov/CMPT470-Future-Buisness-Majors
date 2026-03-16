import random
from datasets import load_dataset

NUM_PAIRS = 20

def build_prompt(code1, code2):
    return f"""
Are these two Java functions similar?

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

print("[INFO] Loading BigCloneBench dataset...")

dataset = load_dataset(
    "google/code_x_glue_cc_clone_detection_big_clone_bench",
    split="test"
)

print(f"[INFO] Dataset size: {len(dataset)}")

indices = random.sample(range(len(dataset)), NUM_PAIRS)
subset = [dataset[i] for i in indices]

print(f"[INFO] Sampled {NUM_PAIRS} pairs\n")

pair_idx = 1

for example in subset:

    prompt = build_prompt(example["func1"], example["func2"])

    print("="*80)
    print(f"PAIR {pair_idx}")
    print("="*80)

    print(prompt)

    print("\n[GROUND TRUTH]")
    print("YES" if example["label"] == 1 else "NO")

    pair_idx += 1

    input("\nPress ENTER to show the next pair...")
