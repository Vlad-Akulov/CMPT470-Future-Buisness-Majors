import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# file path
FILE = "results.xlsx"

# load spreadsheet
df = pd.read_excel(FILE)

# first column = expected, second = predicted
y_true = df.iloc[1:,0].str.upper().str.strip()
y_pred = df.iloc[1:,1].str.upper().str.strip()

# convert YES/NO → 1/0
y_true = y_true.map({"YES":1, "NO":0})
y_pred = y_pred.map({"YES":1, "NO":0})

# metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, zero_division=0)
recall = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)

cm = confusion_matrix(y_true, y_pred)

print("Results")
print("-------")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

print("\nConfusion Matrix")
print("[[TN FP]")
print(" [FN TP]]")
print(cm)
