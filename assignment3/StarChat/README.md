# StarChat-B-16B

---

StarChat-B-16B: A Large Language Model developed for coding help. 
[Article Here](https://drive.google.com/file/d/1cN-b9GnWtHzQRoE7M7gAEyivY0kl4BYs/view)
Authors: Raymond Li et al.

---

### Artifact Discovery and Verification

- The original paper did not include code clone detection benchmarks to compare with. It can be found in the starcoder github page linked here: https://github.com/bigcode-project/starcoder
- This paper benchmarks starchat's ability to write, correct, and fill in code in multiple languages using multiple datasets but does not benchmark code clone detection

---


### Environment Setup

- Used Ubuntu 22.04 through WSL in Windows 11
- PyTorch cu130 in order to run on newer blackwell NVIDIA GPU
- transformers for tokenizer and model loading
- sklearn for metrics calculations
- datasets for the load_dataset tool in order to access the BigCloneBench from google/code_x_glue_cc_clone_detection_big_clone_bench"
- random to randomly select a portion of the dataset
- This environment setup worked immidiately without any extra steps

---

### Smoke Testing

- For a smoke test i simply loaded the starchat model and prompted it to write a python function that adds two numbers. This test worked flawlesly and took about a minute to execute.

program output:

Loading tokenizer...
Loading model...
Loading weights: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 484/484 [00:33<00:00, 14.47it/s]
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Model loaded successfully
Generating output...
Setting `pad_token_id` to `eos_token_id`:0 for open-end generation.

Generated Text:

Write a Python function that adds two numbers.<|end|>
<|assistant|>
Here is a Python function that adds two numbers:

```python
def add_numbers(a, b):
    return a + b
```

This function takes two arguments, `a` and `b`,

---

### Benchmarking

- Used BigCloneBench to test for all clone types (type-1, 2, and 3) with 500 random pairs
- Also tried GPTCloneBench to test multiple languages and semantic clones with 500 random pairs
    - Note: GPTCloneBench provided only true clones which resulted in 0 false positives.

---

### Result Assessment

Since the original paper never tried code clone detection we're unable to compare results with the original benchmark.

The results for BigCloneBench are shown below:

For 500 pairs:

Accuracy : 0.726

Precision : 0.181818

Recall : 0.24324

From these results we can see decent accuracy however you'll notice the precision and recall are very low. This is because the BigCloneBench dataset has many more False clones then True clones. The model generally preferred to answer False which created the ok accuracy score. However this also resulted in many false negatives which lowered the overall performance.

The results for GPTCloneBench are shown below:

For 500 pairs:

Accuracy : 0.142

Precision : 1.0

Recall : 0.142

As mentioned earlier, the GPTCloneBench only provided true pairs. This means that there were 0 false negatives which resulted in the perfect percision. The model only predicted 14.2% of the code pairs correclty which is very bad.

---

### TES Grade

Based on the very unimpressive results, I'm inclined to give this tool a TES-E grade, meaning that the tool was executable with divergent results. However, since the tool was never designed to be a clone detection tool and the paper never benchmarks it for that, I'll give this tool a TES grade of TES-A because it worked as expected and created a baseline for clone detection.


---