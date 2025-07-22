import numpy as np
import mss
import os
from TestsData import TestData
from pathlib import Path

# --------------------------------------
# Color and Image Utilities
# --------------------------------------

def get_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def get_color_at_pos(x, y):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": 1, "height": 1}
        img = sct.grab(monitor)
        color = np.array(img)[0, 0][:3]  # BGR order
        rgb = tuple(int(c) for c in color[::-1])  # convert to RGB
        return rgb
    
# --------------------------------------
# File operations
# --------------------------------------

def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        try:
            with open(file_path, "x") as file:
                pass
        except Exception as e:
            print(f"[ERROR] occurred while creating file : {e}")
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] '{file_path}' not found")
    except Exception as e:
        print(f"[ERROR] while reading file : {e}")

def write_file(file_path: str, content: str):
    try:
        with open(file_path, "w") as file:
            file.write(content.strip())
    except FileNotFoundError:
        print(f"[ERROR] '{file_path}' not found")
    except Exception as e:
        print(f"[ERROR] while writing on file : {e}")

def ref_file_exist(test_data: TestData) -> bool:
    ref_file_path = test_data.get_ref_file_path()
    if not ref_file_path or not ref_file_path.exists():
        print(f"[DEBUG] Reference file '{ref_file_path}' does not exist.")
        return False
    return True