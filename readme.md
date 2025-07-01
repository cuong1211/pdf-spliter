# PDF Processing System 📄🔧

Hệ thống tự động xử lý và chia tách file PDF dựa trên cấu hình JSON, cho phép tách nhiều phần khác nhau từ một file PDF gốc và phân loại theo kiểu tài liệu.

## 🎯 Tính năng chính

- **Tạo template JSON tự động**: Tự động tạo file cấu hình cho mỗi PDF
- **Chia tách PDF linh hoạt**: Tách PDF theo trang hoặc khoảng trang
- **Phân loại tài liệu**: Tự động phân loại và đếm theo loại tài liệu
- **Báo cáo thống kê**: Xuất báo cáo Excel với số lượng từng loại tài liệu
- **Xử lý hàng loạt**: Xử lý nhiều file PDF cùng lúc

## 📋 Yêu cầu hệ thống

### Python Libraries
```bash
pip install PyPDF2 pandas openpyxl
```

### Cấu trúc thư mục
```
project/
├── generate_templates.py    # Script tạo template JSON
├── process_pdfs.py         # Script xử lý PDF
├── input/                  # Thư mục chứa file PDF gốc
├── configs/               # Thư mục chứa file cấu hình JSON
└── output/               # Thư mục chứa kết quả
    ├── [pdf_id]/        # Thư mục con cho mỗi PDF
    └── summary.xlsx     # Báo cáo thống kê
```

## 🚀 Cách sử dụng

### Bước 1: Chuẩn bị file PDF
Đặt tất cả file PDF cần xử lý vào thư mục `input/`

### Bước 2: Tạo template cấu hình
```bash
python generate_templates.py
```

Script này sẽ:
- Quét tất cả file PDF trong thư mục `input/`
- Tạo file JSON tương ứng trong thư mục `configs/`
- Mỗi JSON chứa template cấu hình cần chỉnh sửa

### Bước 3: Chỉnh sửa cấu hình JSON

Mở các file JSON trong `configs/` và chỉnh sửa theo nhu cầu:

```json
{
    "docs_name": "document.pdf",
    "id": 123456789,
    "data": [
        {
            "file_name": "cover_page",
            "number_page": "1",
            "type": "cover"
        },
        {
            "file_name": "content_section",
            "number_page": "2-5",
            "type": "content"
        },
        {
            "file_name": "appendix",
            "number_page": "6,8-10",
            "type": "appendix"
        }
    ]
}
```

### Bước 4: Xử lý PDF
```bash
python process_pdfs.py
```

Script này sẽ:
- Đọc tất cả cấu hình JSON
- Chia tách PDF theo cấu hình
- Tạo file mới trong thư mục output
- Xuất báo cáo thống kê

## ⚙️ Cấu hình JSON chi tiết

### Cấu trúc file JSON:

```json
{
    "docs_name": "tên_file.pdf",     // Tên file PDF gốc
    "id": 123456789,                 // ID duy nhất (tự động tạo)
    "data": [                        // Mảng các phần cần tách
        {
            "file_name": "tên_file_output",    // Tên file đầu ra
            "number_page": "khoảng_trang",     // Trang cần tách
            "type": "loại_tài_liệu"           // Phân loại tài liệu
        }
    ]
}
```

### Cú pháp khoảng trang:

- **Trang đơn**: `"1"` - Chỉ trang 1
- **Khoảng trang**: `"2-5"` - Từ trang 2 đến 5
- **Nhiều khoảng**: `"1,3-5,7"` - Trang 1, từ 3-5, và trang 7
- **Kết hợp**: `"1,3,5-8,10"` - Linh hoạt kết hợp các cách trên

### Ví dụ thực tế:

```json
{
    "docs_name": "bao_cao_tai_chinh_2024.pdf",
    "id": 987654321,
    "data": [
        {
            "file_name": "bia_bao_cao",
            "number_page": "1",
            "type": "cover"
        },
        {
            "file_name": "tom_tat_dieu_hanh",
            "number_page": "2-3", 
            "type": "summary"
        },
        {
            "file_name": "bang_can_doi_ke_toan",
            "number_page": "4-8",
            "type": "financial_statement"
        },
        {
            "file_name": "chu_thich_bao_cao",
            "number_page": "9-15",
            "type": "notes"
        },
        {
            "file_name": "ket_luan_kien_nghi",
            "number_page": "16",
            "type": "conclusion"
        }
    ]
}
```

## 📊 Kết quả đầu ra

### Cấu trúc thư mục output:
```
output/
├── 123456789/                    # ID của PDF đầu tiên
│   ├── cover_page_cover.pdf
│   ├── content_section_content.pdf
│   └── appendix_appendix.pdf
├── 987654321/                    # ID của PDF thứ hai  
│   ├── bia_bao_cao_cover.pdf
│   ├── tom_tat_dieu_hanh_summary.pdf
│   └── ...
└── summary.xlsx                  # Báo cáo thống kê
```

### Báo cáo thống kê (summary.xlsx):
| Type | Count |
|------|-------|
| cover | 5 |
| content | 12 |
| appendix | 3 |
| summary | 8 |

## 🔧 Scripts chi tiết

### 1. generate_templates.py

**Chức năng:**
- Quét thư mục `input/` để tìm file PDF
- Tạo file JSON template cho mỗi PDF
- Tránh ghi đè file JSON đã tồn tại
- Tạo ID duy nhất bằng MD5 hash

**Output mẫu:**
```
✅ Tạo file config: configs/document1.json
✅ Tạo file config: configs/document2.json
⚠️ Đã tồn tại: configs/document3.json, bỏ qua
```

### 2. process_pdfs.py

**Chức năng:**
- Đọc tất cả file JSON trong `configs/`
- Chia tách PDF theo cấu hình
- Tạo thư mục riêng cho mỗi PDF (theo ID)
- Đếm và thống kê loại tài liệu
- Xuất báo cáo Excel

**Output mẫu:**
```
✅ Đã tách: cover_page_cover.pdf (trang 1)
✅ Đã tách: content_section_content.pdf (trang 2-5)
⚠️ Bỏ qua khoảng 15-20 vì không hợp lệ trong document.pdf
✅ Đã ghi thống kê ra: output/summary.xlsx
```

## 🛠️ Troubleshooting

### Lỗi thường gặp:

1. **"Không tìm thấy file PDF"**
   ```
   ❌ Không tìm thấy file PDF: document.pdf
   ```
   - Kiểm tra file PDF có trong thư mục `input/`
   - Đảm bảo tên file trong JSON trùng với file thực tế

2. **"Bỏ qua khoảng trang không hợp lệ"**
   ```
   ⚠️ Bỏ qua khoảng 15-20 vì không hợp lệ trong document.pdf
   ```
   - Kiểm tra số trang trong cấu hình có vượt quá tổng số trang PDF
   - Đảm bảo cú pháp khoảng trang đúng format

3. **Lỗi encoding**
   - Đảm bảo file JSON được lưu với encoding UTF-8
   - Kiểm tra tên file không chứa ký tự đặc biệt

### Debug tips:

- Kiểm tra log chi tiết khi chạy script
- Xác minh cấu hình JSON bằng JSON validator
- Test với file PDF nhỏ trước khi xử lý hàng loạt

## 📝 Tùy chỉnh và mở rộng

### Thay đổi thư mục:
```python
# Trong generate_templates.py
generate_json_templates("my_input", "my_configs")

# Trong process_pdfs.py  
process_all_configs("my_input", "my_configs", "my_output")
```

### Thêm metadata:
```python
# Có thể mở rộng template JSON
template = {
    "docs_name": filename,
    "id": doc_id,
    "created_date": datetime.now().isoformat(),
    "version": "1.0",
    "data": [...]
}
```

### Custom báo cáo:
```python
# Thêm thông tin chi tiết vào báo cáo
df = pd.DataFrame([
    {"Type": doc_type, "Count": count, "Percentage": count/total*100}
    for doc_type, count in type_counter.items()
])
```

## 🚀 Workflow khuyến nghị

1. **Chuẩn bị**: Đặt file PDF vào `input/`
2. **Tạo template**: Chạy `generate_templates.py`
3. **Cấu hình**: Chỉnh sửa file JSON theo nhu cầu
4. **Xử lý**: Chạy `process_pdfs.py`
5. **Kiểm tra**: Xem kết quả trong `output/` và `summary.xlsx`

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa.

## 🤝 Đóng góp

Mọi đóng góp cải thiện hệ thống đều được hoan nghênh!

## 📞 Hỗ trợ

Khi gặp vấn đề:
1. Kiểm tra log và thông báo lỗi
2. Xem phần Troubleshooting
3. Đảm bảo cấu hình JSON đúng format
4. Test với dữ liệu mẫu nhỏ trước
