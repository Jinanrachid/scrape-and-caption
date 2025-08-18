import os
import csv
from application.backend.claude_model import generate_caption

#  Set the folder to process
folder = "Task1/under_1000"

# Process the single folder
results = []
print(f"Processing folder: {folder}")

for file_name in os.listdir(folder):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(folder, file_name)
        print(f"Generating caption for: {file_name}")
        with open(img_path, "rb") as img_file:
            caption = generate_caption(img_file)
            if caption:
                results.append({"image_name": file_name, "caption": caption})

# Save results to CSV in the same folder
csv_path = os.path.join(folder, "captions.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["image_name", "caption"])
    writer.writeheader()
    writer.writerows(results)

print(f" Saved captions to: {csv_path}")
