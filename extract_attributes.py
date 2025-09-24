import os
import re
import json

def extract_entities(text):
    entities = {}

    # 1. Invoice Number / Job Card ID
    entities["Invoice/JobCard ID"] = re.findall(
        r"(?:Invoice\s*No[:\-]?\s*|Job\s*Card\s*ID[:\-]?\s*)([A-Za-z0-9\-\/]+)", 
        text, flags=re.IGNORECASE
    )

    # 2. Dates
    date_patterns = [
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",        
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}",    
    ]
    entities["Date"] = []
    for pat in date_patterns:
        entities["Date"].extend(re.findall(pat, text))

    # 3. Amount / Cost
    entities["Amount"] = re.findall(r"(?:₹|Rs\.?|INR)\s?[\d,]+\.?\d*", text)

    # 4. Emails
    email_regex = r"[a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*[a-z]{2,}"
    raw_emails = re.findall(email_regex, text)
    entities["Email"] = [re.sub(r"\s+", "", e) for e in raw_emails]

    # 5. Phone Numbers
    entities["Phone"] = re.findall(r"(?:\+91[\-\s]?)?\d{10}", text)

    # 6. GST / Tax Number
    entities["GST/Tax"] = re.findall(
        r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b", 
        text, flags=re.IGNORECASE
    )

    # 7. Fitness Certificate Status
    entities["Fitness Certificate Status"] = re.findall(
        r"\b(Valid|Expired|Pending)\b", text, flags=re.IGNORECASE
    )

    # 8. Job Card Status
    entities["Job Card Status"] = re.findall(
        r"\b(Completed|Pending|In Progress)\b", text, flags=re.IGNORECASE
    )

    # 9. Branding / Vendor / Contractor Name
    entities["Branding/Vendor"] = re.findall(
    r"(?:provider|contractor|vendor|company|services)[:,]?\s*([A-Z][A-Za-z0-9\s&.,\-]*(?:Pvt\.?\s*Ltd\.?|Ltd\.?|Contractors?|Enterprises?|Services|Industries?))",
    text,
    flags=re.IGNORECASE
    )

    # 10. Train / Coach Number
    entities["Train/Coach Number"] = re.findall(
        r"(?:Train|Coach)[:\-]?\s*([A-Za-z0-9\-]+)", 
        text, flags=re.IGNORECASE
    )

    # 11. Expiry Dates
    entities["Expiry Dates"] = re.findall(
        r"(?:Expiry|Valid\s*Till|Expires)[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})", 
        text, flags=re.IGNORECASE
    )

    # 12. Address / Location
    address_lines = re.findall(
        r"(?:Depot|Station|Workshop|Vendor|Address)[:\-]?\s*([A-Za-z0-9\s,.-]+)", 
        text, flags=re.IGNORECASE
    )
    entities["Address/Location"] = [line.strip() for line in address_lines]

    return entities


def save_entities_to_text(entities, output_file):
    # Create output folder if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for key, values in entities.items():
            f.write(f"{key}:\n")
            if values:
                for v in values:
                    f.write(f"  - {v}\n")
            else:
                f.write("  - None\n")
            f.write("\n")


if __name__ == "__main__":
    input_folder = "extracted_texts"   # from extract_text.py
    output_folder = "extracted_attributes"

    for file in os.listdir(input_folder):
        if file.endswith(".txt"):
            file_path = os.path.join(input_folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            entities = extract_entities(text)
            print(f"----- Extracted Entities from {file} -----")
            print(json.dumps(entities, ensure_ascii=False, indent=4))

            output_file = os.path.join(output_folder, f"{file.replace('.txt','')}_entities.txt")
            save_entities_to_text(entities, output_file)
