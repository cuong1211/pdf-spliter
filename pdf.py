import os
import json
from PyPDF2 import PdfReader, PdfWriter
from collections import defaultdict
import pandas as pd

def parse_ranges(range_str):
    ranges = []
    for part in range_str.split(','):
        if '-' in part:
            start, end = map(int, part.strip().split('-'))
            ranges.append((start, end))
        else:
            page = int(part.strip())
            ranges.append((page, page))
    return ranges

def split_pdf(file_path, output_dir, entry):
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)

        ranges = parse_ranges(entry["number_page"])
        file_name = entry["file_name"]
        doc_type = entry.get("type", "unknown")

        for start, end in ranges:
            start_index = max(start - 1, 0)
            end_index = min(end, total_pages)

            if start_index >= end_index:
                print(f"⚠️ Bỏ qua khoảng {start}-{end} vì không hợp lệ trong {file_path}")
                continue

            writer = PdfWriter()
            for i in range(start_index, end_index):
                writer.add_page(reader.pages[i])

            output_filename = f"{file_name}_{doc_type}.pdf"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

        return doc_type

    except Exception as e:
        print(f"❌ Lỗi khi xử lý {file_path}: {e}")
        return None

def process_all_configs(input_folder, config_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    type_counter = defaultdict(int)

    for config_file in os.listdir(config_folder):
        if not config_file.endswith('.json'):
            continue

        config_path = os.path.join(config_folder, config_file)
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        pdf_name = config["docs_name"]
        pdf_id = str(config["id"])
        data_entries = config["data"]
        input_pdf_path = os.path.join(input_folder, pdf_name)

        if not os.path.exists(input_pdf_path):
            print(f"❌ Không tìm thấy file PDF: {pdf_name}")
            continue

        output_dir = os.path.join(output_folder, pdf_id)
        os.makedirs(output_dir, exist_ok=True)

        for entry in data_entries:
            doc_type = split_pdf(input_pdf_path, output_dir, entry)
            if doc_type:
                type_counter[doc_type] += 1

    # Ghi thống kê ra file Excel
    if type_counter:
        df = pd.DataFrame(list(type_counter.items()), columns=["Type", "Count"])
        df.to_excel(os.path.join(output_folder, "summary.xlsx"), index=False)
        print(f"✅ Đã ghi thống kê ra: {os.path.join(output_folder, 'summary.xlsx')}")

if __name__ == "__main__":
    process_all_configs("input", "configs", "output")
