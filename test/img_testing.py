import cv2
import base64
import flet as ft
import numpy as np
from io import BytesIO
from PIL import Image
import tempfile
import logging

# Convert OpenCV image (numpy array) to base64
def cv2_to_base64(img):
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    # return f"data:image/png;base64,{base64_img}"
    return base64_img

# Flet UI
def main(page: ft.Page):
    logging.basicConfig(level=logging.DEBUG)
    img = cv2.imread("assets/img/chess.png")
    img_base64 = cv2_to_base64(img)
    page.add(ft.Image(src_base64=img_base64))
    logging.getLogger("flet_core").setLevel(logging.INFO)

ft.app(target=main, assets_dir="assets")


# def format_temp_img(img_cv: np.ndarray, temp_img_path: str) -> str:
#     img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
#     pil_img = Image.fromarray(img_rgb)
#     pil_img.save(temp_img_path, format="PNG")
# def format_img(img_cv: np.ndarray) -> str:
#     # img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
#     # pil_img = Image.fromarray(img_rgb)
#     # buffer = BytesIO()
#     # pil_img.save(buffer, format="PNG")
#     # base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
#     # return base64_img
#     _, buffer = cv2.imencode('.png', img_cv)
#     b64_str = base64.b64encode(buffer).decode('utf-8')
#     return b64_str

# def format_img(img_cv: np.ndarray, format: str = "png") -> str:
#     if len(img_cv.shape) == 3 and img_cv.shape[2] == 3:
#         img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
#     else:
#         img_cv_rgb = img_cv
#     is_success, buffer = cv2.imencode(f".{format}", img_cv_rgb)
#     if not is_success:
#         raise Exception("Could not encode image to buffer.")
#     base64_string = base64.b64encode(buffer).decode("utf-8")
#     return f"data:image/{format};base64,{base64_string}"

# TEMP_IMAGE_FILE = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
# TEMP_IMAGE_PATH = TEMP_IMAGE_FILE.name
# TEMP_IMAGE_FILE.close()

# def main(page: ft.Page):
#     img_cv = cv2.imread("assets/img/chess.png")
#     img_cv = cv2.resize(img_cv, (400, 300))
#     temp_img_path = format_temp_img(img_cv, TEMP_IMAGE_PATH)
#     print("Temp image path:", temp_img_path)

#     page.add(
#         ft.Container(
#             content=ft.Image(
#                 src=temp_img_path,
#                 fit=ft.ImageFit.CONTAIN,
#                 expand=True,
#             ),
#             bgcolor=ft.Colors.BLACK,
#             expand=True,
#         )
#     )

# ft.app(target=main, assets_dir="assets")