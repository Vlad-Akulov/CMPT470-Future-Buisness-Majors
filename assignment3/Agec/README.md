# AGEC

Agec: An execution-semantic clone detection tool
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6613854
(This one isnt public you have to sign in to you usask account to see it on IEEE Xplore)

---

### Artifact Discovery and Verification


1. Ctrl + F github 
    - Found a section that claims its being hosted at https://github.com/tos-kamiyalagec/agec 
    - Following the link on 2026-02-02 shows a broken page dead end
2. Article Claims the tool was applied to an open source product named ArgoUML
    - Found it linked https://argouml.tigris.orgl/
    - Following the link on 2026-02-02 shows a broken page dead end
3. Google Search for the github page 
    - We see a hit under the same authors name seems they created a seperate account named tos-kamiyalagec to host the application untill they archived it on 2018-03-07 https://github.com/tos-kamiya/agec
    - There seems to be an update to the code and the repo seems to have moved to https://github.com/tos-kamiya/agec2/ but the only fixes seem to be documentation and semantic so we will proceed with the original repo

---


### Environment Setup

1. Taking a look at the repository, we see that it consists of 92% Python, 6% ASM, and 1.4% Java. This indicates a Python-based tool that operates on Java programs by compiling them to bytecode and disassembling that bytecode for analysis. The ASM files corresponding to Java bytecode disassembly.

2. Since I am on Windows 10, I created a Python (version 3.12.10) virtual environment and cloned the tool. I used my preinstalled Java SDK (Java SE 25.0.2 (build 25.0.2+10-LTS-69)) to provide the required Java-specific tools (javac and javap) needed for compilation and bytecode disassembly.

3. I had to remove the installer configured java include directory from path to put its bin into path because javap was not included in the javainclude directory 

4. With the setup out of the way we clone the above mentioned repo.

---

### Smoke Testing

1. There were no provided instructions outside of a 1 time exececution so were going to do some interpolating. 

2. Following the posted repo example I'm going to compile the provided ShowWeekday.java project inside of test

3. Not mentioned in the instructions if I should premake the disasm dir so I will in good faith make one ```mkdir .\src\disasm```

4. Now disasemble ```javap -c -p -l -constants ShowWeekdayR > ..\..\..\src\disasm\ShowWeekdayR.asm``` as shown in the project repo but were disasembling to the tool directory so its easier to run on windows without modifying path a whole bunch.

5. Generate n-grams of method invocations ```gen_ngram.py -a disasm > ngrams.txt```.

    - Here we see our first real issue 
    ```
    C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src>python gen_ngram.py -a disasm > ngrams.txt
    Traceback (most recent call last):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\gen_ngram.py", line 478, in <module>
        main(sys.argv)
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\gen_ngram.py", line 363, in main
        for asm_file, sig, code, etbl, ltbl in am.get_method_code_and_tables_iter(asmdir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 162, in get_method_code_and_tables_iter
        for claz, method_sig, body, asm_file in split_into_method_iter_from_asmdir(asm_dir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 159, in split_into_method_iter_from_asmdir
        for v in split_into_method_iter(asmfile, lines):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 90, in split_into_method_iter
        raise AssertionError("unexpected line: %s: %d: %s" % (asmfile, ln + 1, L))
    AssertionError: unexpected line: disasm\ShowWeekdayR.asm: 4:
    ```
    - It looks like the parsing logic is expecting a hardcoded structure from an older java sdk so im going to try to downgrade my sdk

6. Downgrade Java SDK from Java 25 to Java 8 which would have been the most popular/stable release in 2018

7. Repeat up to step 6 with the Java 8 SDK and encounter a new error this time I had no Idea what it was and asking an LLM suggested that on Java 8 with windws redirects could be UTF-16 LE instead of UTF8 which could have been the default on the Operating system the OP was using

    ```
    Traceback (most recent call last):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\gen_ngram.py", line 478, in <module>
        main(sys.argv)
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\gen_ngram.py", line 363, in main
        for asm_file, sig, code, etbl, ltbl in am.get_method_code_and_tables_iter(asmdir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 162, in get_method_code_and_tables_iter
        for claz, method_sig, body, asm_file in split_into_method_iter_from_asmdir(asm_dir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 158, in split_into_method_iter_from_asmdir
        for asmfile, lines in asm_filetext_iter(asmdir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 30, in asm_filetext_iter
        lines = f.read().decode('utf-8').split('\n')
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

    ```
8. Opening the asm file in a notepad file suggests that the LLM was correct and the encoding is in fact UTF-16 LE. If you plan on reproducing this I suggest using a normal opperating system like debian. 

9. Go back and regenerate the same thing again with a javap flag for utf8 
    ```
    javap -J-Dfile.encoding=UTF-8 -c -p -l -constants ShowWeekdayR > ..\..\..\src\disasm\ShowWeekdayR.asm
    ```

10. Checking the encoding type is now correctly utf8 we see that ....... the original error has returned even with an older version of the Java sdk 

    ```
        C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src>python gen_ngram.py -a disasm > ngrams.txt
    Traceback (most recent call last):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\gen_ngram.py", line 478, in <module>
        main(sys.argv)
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\gen_ngram.py", line 363, in main
        for asm_file, sig, code, etbl, ltbl in am.get_method_code_and_tables_iter(asmdir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 162, in get_method_code_and_tables_iter
        for claz, method_sig, body, asm_file in split_into_method_iter_from_asmdir(asm_dir):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 159, in split_into_method_iter_from_asmdir
        for v in split_into_method_iter(asmfile, lines):
    File "C:\Users\gostg\Documents\vscode\470\CMPT470-Future-Buisness-Majors\assignment3\Agec\agec\src\asm_manip.py", line 90, in split_into_method_iter
        raise AssertionError("unexpected line: %s: %d: %s" % (asmfile, ln + 1, L))
    AssertionError: unexpected line: disasm\ShowWeekdayR.asm: 4:
    ```

11. This is about as far as my good faith extends we are marking this TES-C as it fails mid execution
---

### Benchmarking

CLONE TYPE: Semantic Code-Clone detection for Java so we would be using SemanticCloneBench had the tool worked properly

---

### Result Assessment

The paper did not provide any precision/recall metrics which is fine since this is a semantic tool and typically dosent have objective precision/recall metrics.

Unfortunately since we could not get the tool working we cannot comment on the results.


| TES Grade | Description |
|---|---|
| **TES-C (Partially Executable)** | The tool did not complete the full intended workflow, even after substantial effort. This includes cases where the tool ran only basic commands or smoke tests, failed on realistic benchmarks, crashed mid-execution, or produced incomplete or unreliable outputs. |

---