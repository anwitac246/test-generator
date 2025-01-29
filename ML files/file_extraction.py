import os
import fitz  
import re
import json
from PIL import Image
from io import BytesIO

def extract_and_chunk_with_context(pdf_path, output_folder, target_size=(224, 224)):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    extracted_data = []
    heading_regex = r"^[A-Z][A-Z0-9\s\-:]+$"
    supported_formats = ["jpeg", "jpg", "png"]
    current_chunk = {"type": "text", "content": "", "context": ""}
    current_heading = None

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text("text")
        lines = page_text.split("\n")
        for line in lines:
            if re.match(heading_regex, line.strip()):  
                if current_chunk["content"].strip():
                    extracted_data.append(current_chunk)
                    current_chunk = {"type": "text", "content": "", "context": ""}
                current_heading = line.strip()
                current_chunk["context"] = f"{current_heading} (Page {page_num + 1})"
            else:
                current_chunk["content"] += line + " "

       
        for img_idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image.get("image")
            image_ext = base_image.get("ext", "unknown").lower()

            if not image_bytes or image_ext not in supported_formats:
                print(f"Skipping unsupported or invalid image on Page {page_num + 1}, Image {img_idx + 1} (Format: {image_ext})")
                continue

            try:
              
                image = Image.open(BytesIO(image_bytes)).convert("RGB")
                image_resized = image.resize(target_size, Image.Resampling.LANCZOS)

                
                image_filename = f"page_{page_num + 1}_img_{img_idx + 1}.{image_ext}"
                image_path = os.path.join(output_folder, image_filename)
                image_resized.save(image_path)

            
                image_context = f"{current_heading or 'Page'} {page_num + 1}: Image {img_idx + 1}"
                extracted_data.append({
                    "type": "image",
                    "content": image_path,
                    "page_no": page_num + 1,
                    "context": image_context
                })
            except Exception as e:
                print(f"Error processing image on Page {page_num + 1}, Image {img_idx + 1}: {e}")
                continue

  
    if current_chunk["content"].strip():
        extracted_data.append(current_chunk)

    return extracted_data



pdf_path = r"D:\Projects\test-generator-llm-rag\jee-content\pyq\dokumen.pub_43-years-jee-advanced-1978-2020-jee-main-chapterwise-amp-topicwise-solved-papers-chemistry-16nbsped-8194767733-9788194767732.pdf"
output_folder = r"D:/Projects/test-generator-llm-rag/output_folder/PYQ16"
target_size = (224, 224)

chunked_data = extract_and_chunk_with_context(pdf_path, output_folder, target_size=target_size)

with open(os.path.join(output_folder, "chunked_data.json"), "w", encoding="utf-8") as f:
    json.dump(chunked_data, f, indent=4)

print("Extraction, preprocessing, and context-aware chunking complete!")
