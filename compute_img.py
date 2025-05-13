import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

def load_img(img_name: str) -> np.ndarray:
    img = cv2.imread('img/'+img_name)
    if img is None:
        raise FileNotFoundError(f"Image not found at {img_name}")
    return img

###########################
# SIMILARITY
###########################

def calculate_similarity(img_reference: np.ndarray, img_comparison: np.ndarray) -> tuple[float, np.ndarray]:
    ssim_scores = []
    # diff_list = []

    # Calculate SSIM for each color channel
    for i in range(3):
        score, channel_diff = ssim(img_reference[:, :, i], img_comparison[:, :, i], full=True)
        ssim_scores.append(score)
        # diff_list.append(channel_diff)

    mean_ssim = np.mean(ssim_scores)
    # diff = np.max(diff_list, axis=0)
    diff = channel_diff
    # Convert the diff image to uint8 (make it useful for visualization)
    diff = (1.0 - diff)
    diff = (diff * 255).astype("uint8")
    return mean_ssim, diff

def calculate_similarity_2(img_reference: np.ndarray, img_comparison: np.ndarray) -> tuple[float, np.ndarray]:
    diff = cv2.absdiff(img_reference, img_comparison)
    mean_ssim = 1.0 - (np.mean(diff) / 255.0)
    return mean_ssim, diff

###########################
# PROCESSING
###########################

def process_difference(diff: np.ndarray, img_reference: np.ndarray, img_comparison: np.ndarray) -> dict[str, np.ndarray]:
    # calculate the threshold for the difference image with otsu method and ignore the 0 value of the thresh
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # compatibility with OpenCV 4.x and 3.x
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(img_reference.shape, dtype='uint8')
    filled = img_comparison.copy()
    outlined = img_comparison.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 1: # size of the relevant contours
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(outlined, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled, [c], 0, (0,255,0), -1)

    return {
        'thresh': thresh,
        'mask': mask,
        'outlined': outlined,
        'filled': filled,
    }

def process_difference_2(diff: np.ndarray, img_reference: np.ndarray, img_comparison: np.ndarray) -> dict[str, np.ndarray]:
    _, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)  # adjust second parameter for sensitivity

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(img_reference.shape, dtype='uint8')
    filled = img_comparison.copy()
    outlined = img_comparison.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 1:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(outlined, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled, [c], 0, (0, 255, 0), -1)

    return {
        'thresh': thresh,
        'mask': mask,
        'outlined': outlined,
        'filled': filled,
    }
def process_difference_3(diff: np.ndarray, img_reference: np.ndarray, img_comparison: np.ndarray) -> dict[str, np.ndarray]:
    b, g, r = cv2.split(diff)
    combined = cv2.max(cv2.max(b, g), r)
    _, thresh = cv2.threshold(combined, 10, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(img_reference.shape, dtype='uint8')
    filled = img_comparison.copy()
    outlined = img_comparison.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 1:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(outlined, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled, [c], 0, (0, 255, 0), -1)

    return {
        'thresh': thresh,
        'mask': mask,
        'outlined': outlined,
        'filled': filled,
    }

###########################
# SHOWING
###########################

def show_all_diff(result_diff: dict[str, np.ndarray], img_reference: np.ndarray, img_comparison: np.ndarray) -> None:
    cv2.imshow("Original Image", img_reference)
    cv2.imshow("Altered Image", img_comparison)
    cv2.imshow("Difference Image", result_diff['thresh'])
    cv2.imshow("Mask Image", result_diff['mask'])
    cv2.imshow("Filled Image", result_diff['filled'])
    cv2.imshow("Outlined Image", result_diff['outlined'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def show_mask(result_diff: dict[str, np.ndarray], img_reference: np.ndarray = None) -> None:
    if img_reference is not None:
        cv2.imshow("Reference Image", img_reference)
    cv2.imshow("Mask Image", result_diff['mask'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def show_filled(result_diff: dict[str, np.ndarray], img_reference: np.ndarray = None) -> None:
    if img_reference is not None:
        cv2.imshow("Reference Image", img_reference)
    cv2.imshow("Filled Image", result_diff['filled'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def show_outlined(result_diff: dict[str, np.ndarray], img_reference: np.ndarray = None) -> None:
    if img_reference is not None:
        cv2.imshow("Reference Image", img_reference)
    cv2.imshow("Outlined Image", result_diff['outlined'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def show_diff(result_diff: dict[str, np.ndarray], img_reference: np.ndarray = None) -> None:
    if img_reference is not None:
        cv2.imshow("Reference Image", img_reference)
    cv2.imshow("Difference Image", result_diff['thresh'])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
