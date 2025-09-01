# 🚀 ProjectDump GUI

ProjectDump là công cụ gom mã nguồn của một project thành một file duy nhất (`source_dump.txt`).  
Phiên bản này đã được bổ sung **giao diện người dùng bằng Tkinter** để dễ thao tác hơn.

---

## ✨ Tính năng
- Tự động phát hiện công nghệ dự án (Python, Node.js, Java, v.v.)
- Lọc bỏ thư mục/file rác (node_modules, build, cache…)
- Tạo **cây thư mục** và trích xuất nội dung code
- Lưu ra file `source_dump.txt` ngay trong project
- Giao diện GUI với:
  - Chọn ngôn ngữ (Tiếng Việt / English)
  - Chọn thư mục dự án
  - Hiển thị log chi tiết
  - Nút mở nhanh thư mục chứa file output

---

## 🖥️ Cách chạy (Python)

### Yêu cầu
- Python 3.8+
- Các thư viện chuẩn (Tkinter, os, sys…) đã có sẵn trong Python

### Chạy trực tiếp
```bash
python __main__.py
```

---

## 📦 Build thành file chạy độc lập

### Windows (exe)
Cài **PyInstaller**:
```bash
pip install pyinstaller
```

Build file `.exe`:
```bash
pyinstaller --onefile --windowed __main__.py -n ProjectDumpGUI
```

Kết quả: `dist/ProjectDumpGUI.exe`

Nếu muốn thêm icon:
```bash
pyinstaller --onefile --windowed --icon=icon.ico __main__.py -n ProjectDumpGUI
```

---

### macOS (app)
Cài **PyInstaller**:
```bash
pip install pyinstaller
```

Build file `.app`:
```bash
pyinstaller --onefile --windowed --name ProjectDumpGUI __main__.py
```

Kết quả: `dist/ProjectDumpGUI.app`

Thêm icon `.icns`:
```bash
pyinstaller --onefile --windowed --icon=icon.icns __main__.py -n ProjectDumpGUI
```

⚠️ **Lưu ý**:
- App chỉ chạy trên cùng kiến trúc máy build (Intel vs Apple Silicon).
- Nếu chia sẻ cho người khác, có thể cần **codesign** và **notarize** với Apple Developer ID.

---

## 📂 File output
Sau khi chạy thành công, file sẽ được tạo tại:
```
<project_path>/source_dump.txt
```

---

## 🎯 Demo giao diện
- Chọn ngôn ngữ (vi/en)
- Chọn thư mục dự án
- Bấm **Chạy ProjectDump**
- Xem log chi tiết trong cửa sổ
- Bấm **Mở thư mục output** để mở ngay thư mục chứa file kết quả

---

## 📜 License
MIT License.
