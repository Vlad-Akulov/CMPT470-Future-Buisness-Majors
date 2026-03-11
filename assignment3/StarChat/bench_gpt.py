import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datasets import load_dataset
import random

MODEL_NAME = "HuggingFaceH4/starchat-beta"

DATASET = "gptclonebench"   # "gptclonebench" or "gcj"
NUM_PAIRS = 500
BATCH_SIZE = 3

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True


print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.padding_side = "left"

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


print("Loading StarChat model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    dtype=torch.float16
)

model.eval()


def build_prompt(code1, code2):
    return f"""
Are these two programs similar?

Respond ONLY with:
YES
or
NO

Program A:
{code1}

Program B:
{code2}

Answer:
"""


def predict_batch(prompts):

    inputs = tokenizer(
        prompts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=8192
    ).to(model.device)

    with torch.inference_mode():
        outputs = model(**inputs)

    logits = outputs.logits[:, -1, :]

    yes_token = tokenizer.encode(" YES", add_special_tokens=False)[0]
    no_token = tokenizer.encode(" NO", add_special_tokens=False)[0]

    preds = []

    for i in range(len(prompts)):

        probs = torch.softmax(logits[i, [yes_token, no_token]], dim=0)

        yes_prob = probs[0].item()
        no_prob = probs[1].item()

        if yes_prob > no_prob:
            preds.append(1)
            print(f"Model output: YES ({yes_prob:.3f})")
        else:
            preds.append(0)
            print(f"Model output: NO ({no_prob:.3f})")

    return preds


########################################
# LOAD DATA
########################################

pairs = []

if DATASET == "gptclonebench":

    print("[INFO] Loading GPTCloneBench...")

    dataset = load_dataset("Reid996/GPTCloneBench", split="All")

    print(f"[INFO] Dataset size: {len(dataset)}")

    indices = random.sample(range(len(dataset)), NUM_PAIRS)

    for i in indices:
        example = dataset[i]

        pairs.append({
            "code1": example["func1"],
            "code2": example["func2"],
            "label": example["label"]
        })


elif DATASET == "gcj":

    print("[INFO] Loading Google Code Jam dataset...")

    dataset = load_dataset("izhx/google-code-jam", split="all")

    print(f"[INFO] Dataset size: {len(dataset)}")

    # group solutions by problem
    problem_map = {}

    for row in dataset:
        pid = row["problem"]
        code = row["code"]

        if pid not in problem_map:
            problem_map[pid] = []

        problem_map[pid].append(code)

    problems = list(problem_map.keys())

    # generate pairs
    for _ in range(NUM_PAIRS):

        if random.random() < 0.5:

            # clone pair
            p = random.choice(problems)

            if len(problem_map[p]) < 2:
                continue

            code1, code2 = random.sample(problem_map[p], 2)

            label = 1

        else:

            # non clone pair
            p1, p2 = random.sample(problems, 2)

            code1 = random.choice(problem_map[p1])
            code2 = random.choice(problem_map[p2])

            label = 0

        pairs.append({
            "code1": code1,
            "code2": code2,
            "label": label
        })


print(f"[INFO] Generated {len(pairs)} pairs")


########################################
# BENCHMARK
########################################

y_true = []
y_pred = []

batch_prompts = []
batch_labels = []

pair_idx = 1

for example in tqdm(pairs):

    prompt = build_prompt(example["code1"], example["code2"])

    batch_prompts.append(prompt)
    batch_labels.append(example["label"])

    if len(batch_prompts) == BATCH_SIZE:

        preds = predict_batch(batch_prompts)

        for p, t in zip(preds, batch_labels):
            y_pred.append(p)
            y_true.append(t)

            print(f"Pair {pair_idx}: Prediction={p}  True={t}")
            pair_idx += 1

        batch_prompts = []
        batch_labels = []


if batch_prompts:

    preds = predict_batch(batch_prompts)

    for p, t in zip(preds, batch_labels):
        y_pred.append(p)
        y_true.append(t)


########################################
# RESULTS
########################################

print("\nBenchmark Results")

acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)

print("Accuracy :", acc)
print("Precision:", prec)
print("Recall   :", rec)
print("F1 Score :", f1)
print("Total evaluated:", len(y_true))