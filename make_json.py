import os
import json
import hashlib

def generate_json_templates(input_folder, config_folder):
    os.makedirs(config_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            name_without_ext = os.path.splitext(filename)[0]
            json_path = os.path.join(config_folder, f"{name_without_ext}.json")

            if not os.path.exists(json_path):  # tránh ghi đè
                # Tạo id bằng cách hash tên file (giữ cho ngắn gọn)
                doc_id = int(hashlib.md5(filename.encode('utf-8')).hexdigest()[:8], 16)

                template = {
                    "docs_name": filename,
                    "id": doc_id,
                    "data": [
                        {
                            "file_name": "example_name",
                            "number_page": "1-2",
                            "type": "example_type"
                        }
                    ]
                }

                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(template, f, indent=4, ensure_ascii=False)

                print(f"✅ Tạo file config: {json_path}")
            else:
                print(f"⚠️ Đã tồn tại: {json_path}, bỏ qua")

if __name__ == "__main__":
    generate_json_templates("input", "configs")
