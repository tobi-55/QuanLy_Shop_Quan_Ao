from cx_Freeze import setup, Executable
import sys

# Thêm các file cần thiết
build_exe_options = {
    "packages": ["tkinter", "json", "os", "hashlib", "requests", "datetime", "threading"],
    "excludes": ["unittest"],
    "include_files": [],
}

# Thiết lập cho Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ClothingShopManager",
    version="1.0",
    description="Ứng dụng Quản lý Shop Quần Áo",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="QuanLyShopQuanAo.exe",
            icon=None
        )
    ],
)