import json
import random

# Load the dataset
with open('KMRL_Operational_Snapshot.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Shuffle the dataset
random.shuffle(dataset)

# Train-test split (80:20)
split_index = int(0.8 * len(dataset))
train_set = dataset[:split_index]
test_set = dataset[split_index:]

# Save to JSON files
with open('KMRL_Operational_Train.json', 'w', encoding='utf-8') as f:
    json.dump(train_set, f, indent=2)

with open('KMRL_Operational_Test.json', 'w', encoding='utf-8') as f:
    json.dump(test_set, f, indent=2)

print(f"Total entries: {len(dataset)}")
print(f"Training set: {len(train_set)} entries")
print(f"Test set: {len(test_set)} entries")
