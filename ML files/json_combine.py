import json
import os
def combine(json_file, output):
    with open(json_file, "r", encoding="utf-8") as file:
        extracted_data = json.load(file)

    combined_data = []
    for entry in extracted_data:
        if entry['type'] =='text':
            combined_entry = f"entry{entry['page']}: {entry['content']}"
            combined_data.append(combined_entry)
        elif (entry['type']=='image'):
            combined_entry = f"entry{entry['page']} - Image: {entry['context']} - Path: {entry['content']}"
            combined_data.append(combined_entry)