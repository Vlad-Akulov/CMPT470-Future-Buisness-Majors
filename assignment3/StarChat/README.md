# StarChat-B-16B

StarChat-B-16B
https://huggingface.co/HuggingFaceH4/starchat-beta

---

### Artifact Discovery and Verification

1. Find the Artifact

https://huggingface.co/HuggingFaceH4/starchat-beta

2. Verify that the artifact corresponds to the tool described in the paper

3. Record the artifact link in the excel document 📝 (under Github Repo)

4. Document how the artifact was discovered (paper link, website, archive)

5. Document Original Recall and/or Precision if it was included in the document 📝

The original paper did not include code clone detection benchmarks to compare with.

---


### Environment Setup

1. Identify required operating system, runtime, and dependencies

I used Ubuntu 22.04 through WSL in Windows 11. I used PyTorch cu130 in order to run on newer blackwell NVIDIA GPU, transformers for tokenizer and model loading, sklearn for metrics calculations, datasets for the load_dataset tool, and random to randomly select a portion of the dataset.

2. Follow original instructions where available

3. Document environment details precisely (Both here and in the excel document 📝)

4. If you had to fix the environment or update dependencies please mention it here

---

### Smoke Testing

1. Attempt Basic execution (e.g., help command or small input)

For a smoke test i simply loaded the starchat model and prompted it to write a python function that adds two numbers. This test worked flawlesly and took about a minute to execute.

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

2. Capture Logs and error messages (e.g. terminal output/screenshots or output files)

---

### Benchmarking

1. Execute the tool on a compatible provided benchmark. (Whichever applies best. NOTE: If your paper specifies a specific testbench not already defined then )

2. Document the tool you used and clone type in the excel document 📝

2. Use default or paper-specified settings 

3. Document the settings you used in the excel document 📝

4. Do not modify algorithms or datasets if it dosent work put in a bit of effort to resolve the issue but dont change source code or toolchain configuration. 

5. As specified by the lab manual: 
**If you are unsure whether an action is allowed, document the issue and stop.**

##### Allowed
    - Searching author websites and archival sources
    - Fixing minor build or dependency issues
    - Updating deprecated libraries
    - Using containers or virtual machines

##### Not Allowed
    - Rewriting detection logic
    - Changing algorithms or evaluation design
    - Tuning parameters beyond what is described in the paper
    - Substituting datasets



| If you want to evaluate… | Then use this benchmark |
|---|---|
| Cross-language clone detection (any clone type) | GoogleCodeJam (cross-language) |
| Cross-language clone detection (modern / LLM-oriented) | GPTCloneBench (cross-language section) |
| Java clone detection only | BigCloneBench |
| Type-1 clones (exact copies, Java) | BigCloneBench |
| Type-2 clones (renamed identifiers, Java) | BigCloneBench |
| Type-3 clones (edited structure, Java) | BigCloneBench |
| Semantic clone detection | SemanticCloneBench |
| Semantic clones in Java, C, C#, Python | SemanticCloneBench |
| Semantic clones with LLM-generated variants | GPTCloneBench |
| Semantic clones in Java, C, C#, Python (LLM-focused) | GPTCloneBench |

---

### Result Assessment

1. Compute precision and recall only if supported

For 500 pairs:
Accuracy : 0.726
Precision : 0.181818
Recall : 0.24324

2. Document Precision and recall in the excel document 📝

3. Extract original metrics from the paper

4. Compare reproduced results with reported results and document it in the excel document 📝 (make sure you also document it here in a bit more depth)

The original paper did not benchmark for code clone detection. This tool is not designed for code clone detection and it's simply an LLM focussed on code generation. The original paper benchmarks for code generation and understanding.

5. Give it a TES Grade and document it in the excel document 📝

| TES Grade | Description |
|---|---|
| **TES-A (Executable)** | The tool executed successfully with minimal effort following the authors’ original instructions. No non-trivial intervention was required beyond routine environment setup, and execution produced the expected outputs on the target benchmark(s). |
| **TES-B (Executable with Intervention)** | The tool successfully completed the full intended workflow and produced complete outputs only after intervention, such as fixing compatibility issues, recovering missing dependencies, or correcting documentation inconsistencies. |
| **TES-C (Partially Executable)** | The tool did not complete the full intended workflow, even after substantial effort. This includes cases where the tool ran only basic commands or smoke tests, failed on realistic benchmarks, crashed mid-execution, or produced incomplete or unreliable outputs. |
| **TES-D (Non-Executable)** | The tool could not be executed despite best-effort attempts. This includes cases where no official artifact was found, the tool failed irrecoverably during build or execution, or critical components were missing with no feasible path to recovery. |
| **TES-E (Executed with Divergent Results)** | The tool executed and produced outputs, but the results deviated substantially from those reported in the original paper, either quantitatively (e.g., lower precision or recall) or qualitatively. |

---