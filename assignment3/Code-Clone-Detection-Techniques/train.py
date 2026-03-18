import random
from datasets import load_dataset

NUM_PAIRS = 30  # must be even

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

# split into YES (1) and NO (0)
clones = [x for x in dataset if x["label"] == 1]
non_clones = [x for x in dataset if x["label"] == 0]

print(f"[INFO] Total clones: {len(clones)}")
print(f"[INFO] Total non-clones: {len(non_clones)}")

half = NUM_PAIRS // 2

# sample equally
sampled_clones = random.sample(clones, half)
sampled_non_clones = random.sample(non_clones, half)

# combine and shuffle
subset = sampled_clones + sampled_non_clones
# random.shuffle(subset)

print(f"[INFO] Sampled {half} YES and {half} NO pairs\n")

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
