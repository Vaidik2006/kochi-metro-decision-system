import json
import os

# Define file paths (assuming same directory)
classification_file = "Classification.json"
summarization_file = "Summarization.json"
extraction_file = "Extraction.json"
output_file = "Full_Pipeline_Dataset.json"

# Load JSON files
with open(classification_file, "r", encoding="utf-8") as f:
    classification_data = json.load(f)

with open(summarization_file, "r", encoding="utf-8") as f:
    summarization_data = json.load(f)

with open(extraction_file, "r", encoding="utf-8") as f:
    extraction_data = json.load(f)

# Convert summarization and extraction to dictionaries keyed by doc_id
summary_dict = {doc["doc_id"]: doc.get("summary") for doc in summarization_data}
entities_dict = {doc["doc_id"]: doc.get("entities") for doc in extraction_data}

# Merge datasets
merged_data = []

for doc in classification_data:
    doc_id = doc["doc_id"]
    doc["summary"] = summary_dict.get(doc_id, None)  # Add summary if available
    doc["entities"] = entities_dict.get(doc_id, None)  # Add entities if available
    merged_data.append(doc)

# Save merged dataset
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, indent=2, ensure_ascii=False)

print(f"Full Pipeline dataset saved as '{output_file}' with {len(merged_data)} entries.")
