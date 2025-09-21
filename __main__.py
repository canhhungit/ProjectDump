import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from aggregator import aggregate_code
from constants import TEXT_VI, TEXT_EN
import io
import contextlib
import subprocess
import platform
import json

CONFIG_FILE = "last_path.json"


def save_last_path(path: str):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_path": path}, f)
    except Exception as e:
        print("Không thể lưu last_path:", e)


def load_last_path() -> str | None:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("last_path")
        except Exception:
            return None
    return None


class ProjectDumpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 ProjectDump")
        self.root.geometry("800x600")

        self.output_path = None  # Lưu lại đường dẫn output để mở

        # Language selection
        tk.Label(root, text="🌐 Ngôn ngữ / Language:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.lang_var = tk.StringVar(value="en")
        lang_menu = ttk.Combobox(root, textvariable=self.lang_var, values=["vi", "en"], state="readonly", width=10)
        lang_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Project path selection
        tk.Label(root, text="📂 Thư mục dự án:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(root, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.choose_folder).grid(row=1, column=2, padx=5, pady=5)

        # 🔄 Load last project path nếu có
        last_path = load_last_path()
        if last_path:
            self.path_var.set(last_path)

        # Run + Open buttons
        tk.Button(root, text="▶️ Chạy ProjectDump", command=self.run_projectdump).grid(
            row=2, column=0, pady=10, padx=10, sticky="w"
        )

        self.open_btn = tk.Button(root, text="📂 Mở thư mục output", command=self.open_output_folder, state="disabled")
        self.open_btn.grid(row=2, column=1, pady=10, sticky="w")

        # Log output area
        tk.Label(root, text="📜 Log output:").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        self.log_text = tk.Text(root, wrap="word", height=25)
        self.log_text.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Scrollbar cho log
        scrollbar = tk.Scrollbar(root, command=self.log_text.yview)
        scrollbar.grid(row=3, column=3, sticky="nsew")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Cho phép layout giãn
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)
            save_last_path(folder)  # 👈 lưu lại ngay khi chọn

    def run_projectdump(self):
        project_path = self.path_var.get().strip() or os.getcwd()
        lang = self.lang_var.get().lower()
        text = TEXT_EN if lang == "en" else TEXT_VI
        project_path = os.path.abspath(project_path)

        # Reset trạng thái
        self.open_btn.config(state="disabled")
        self.output_path = None

        # Redirect stdout/stderr vào log box
        log_buffer = io.StringIO()
        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
            success = aggregate_code(project_path, text)

        # In log ra Text widget
        self.log_text.insert(tk.END, log_buffer.getvalue() + "\n")
        self.log_text.see(tk.END)  # Scroll xuống cuối

        if success:
            self.output_path = os.path.join(project_path, "source_dump.txt")
            self.open_btn.config(state="normal")  # Bật nút mở thư mục
            messagebox.showinfo("✅ Success", text["done"])
        else:
            messagebox.showerror("❌ Error", text["error"])

    def open_output_folder(self):
        if self.output_path and os.path.exists(self.output_path):
            folder = os.path.dirname(self.output_path)
            if platform.system() == "Windows":
                os.startfile(folder)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder])
            else:  # Linux
                subprocess.run(["xdg-open", folder])
        else:
            messagebox.showwarning("⚠️", "Không tìm thấy file output!")


def main():
    root = tk.Tk()
    app = ProjectDumpGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
