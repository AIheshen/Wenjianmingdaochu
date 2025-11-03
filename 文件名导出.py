import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sys

# === 获取默认下载路径 ===
def get_download_path():
    try:
        return os.path.join(os.path.expanduser("~"), "Downloads")
    except Exception:
        return os.path.expanduser("~")

# === 主窗口 ===
root = tk.Tk()
root.title("文件名导出工具")
root.geometry("540x300")
root.resizable(False, False)

# 设置窗口图标
icon_path = os.path.join(os.path.dirname(sys.argv[0]), "文件名导出.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# === 标题与图标 ===
img_path = os.path.join(os.path.dirname(sys.argv[0]), "文件名导出.png")
if os.path.exists(img_path):
    try:
        from PIL import Image, ImageTk
        img = Image.open(img_path).resize((64, 64))
        tk_img = ImageTk.PhotoImage(img)
        tk.Label(root, image=tk_img).place(x=30, y=20)
    except:
        pass

tk.Label(root, text="文件名导出工具", font=("Microsoft YaHei", 16, "bold")).place(x=120, y=35)

# === 变量 ===
folder_var = tk.StringVar()
output_dir_var = tk.StringVar(value=get_download_path())
include_fullpath = tk.BooleanVar(value=False)

# === 选择路径 ===
def choose_folder():
    path = filedialog.askdirectory(title="选择要导出的文件夹")
    if path:
        folder_var.set(path)

def choose_output_folder():
    path = filedialog.askdirectory(title="选择TXT导出保存目录")
    if path:
        output_dir_var.set(path)

# === 导出逻辑 ===
def export_filelist():
    folder = folder_var.get().strip()
    output_dir = output_dir_var.get().strip()

    if not folder or not os.path.isdir(folder):
        messagebox.showwarning("提示", "请选择有效的文件夹路径！")
        return
    if not output_dir or not os.path.isdir(output_dir):
        messagebox.showwarning("提示", "请选择有效的导出目录！")
        return

    folder_name = os.path.basename(os.path.normpath(folder))
    output_file = os.path.join(output_dir, f"{folder_name}（内所有文件名称）.txt")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for root_dir, dirs, files in os.walk(folder):
                level = root_dir.replace(folder, "").count(os.sep)
                indent = "    " * level
                folder_display = os.path.basename(root_dir)
                if folder_display:
                    # 用 emoji 标记文件夹
                    f.write(f"{indent}📂 {folder_display}/\n")

                for file in files:
                    if include_fullpath.get():
                        file_line = os.path.join(root_dir, file)
                    else:
                        file_line = f"{indent}    {file}"
                    f.write(file_line + "\n")

        messagebox.showinfo("完成", f"文件名已导出到：\n{output_file}")
        os.startfile(output_dir)
    except Exception as e:
        messagebox.showerror("错误", f"导出失败：\n{e}")

# === 布局 ===
tk.Label(root, text="选择目标文件夹：", font=("Microsoft YaHei", 10)).place(x=30, y=110)
tk.Entry(root, textvariable=folder_var, width=50).place(x=170, y=110)
ttk.Button(root, text="浏览", command=choose_folder).place(x=450, y=107)

tk.Label(root, text="导出TXT保存目录：", font=("Microsoft YaHei", 10)).place(x=30, y=150)
tk.Entry(root, textvariable=output_dir_var, width=50).place(x=170, y=150)
ttk.Button(root, text="修改", command=choose_output_folder).place(x=450, y=147)

ttk.Checkbutton(root, text="包含完整路径（不缩进）", variable=include_fullpath).place(x=170, y=185)

ttk.Button(root, text="开始导出", command=export_filelist, width=22).place(x=200, y=230)

root.mainloop()
