import json
import random
import os

# Load full pipeline dataset
with open("Full_Pipeline_Dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Shuffle data
random.shuffle(data)

# 80/20 split
split_idx = int(len(data) * 0.8)
train_data = data[:split_idx]
test_data = data[split_idx:]

# Save splits
with open("Full_Pipeline_Train.json", "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2, ensure_ascii=False)

with open("Full_Pipeline_Test.json", "w", encoding="utf-8") as f:
    json.dump(test_data, f, indent=2, ensure_ascii=False)

print(f"Train dataset: {len(train_data)} entries")
print(f"Test dataset: {len(test_data)} entries")
