import os
import sys
import time
import random
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

def main() -> None:
    # Load and launch the projects
    img_comparison = load_img('chess-altered.png')
    img_comparison2 = load_img('chess-altered-hard.png')

    # Load the image database
    img_reference = load_img('chess.png')

    # Compare the outputs and adapt the threshold
    score, diff = calculate_similarity(img_reference, img_comparison)
    print("Average SSIM Grey:", score)
    print("Similarity Score: {:.5f}%".format(score * 100))

    # thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = contours[0] if len(contours) == 2 else contours[1]

    # # Highlight differences
    # mask = np.zeros(img1.shape, dtype='uint8')
    # filled = img2.copy()

    # for c in contours:
    #     area = cv2.contourArea(c)
    #     if area > 100:
    #         x,y,w,h = cv2.boundingRect(c)
    #         cv2.rectangle(img1, (x, y), (x + w, y + h), (36,255,12), 2)
    #         cv2.rectangle(img2, (x, y), (x + w, y + h), (36,255,12), 2)
    #         cv2.drawContours(mask, [c], 0, (0,255,0), -1)
    #         cv2.drawContours(filled, [c], 0, (0,255,0), -1)

    # # cv2.imshow('img1', img1)
    # # cv2.imshow('img2', img2)
    # cv2.imshow('diff', diff)
    # cv2.imshow('mask', mask)
    # cv2.imshow('filled', filled)
    # cv2.waitKey(0)

def load_img(img_name: str) -> any:
    img = cv2.imread('img/'+img_name)
    if img is None:
        raise FileNotFoundError(f"Image not found at {img_name}")
    return img

def calculate_similarity(img_reference, img_comparison) -> tuple:
    ssim_scores = []
    # Calculate SSIM for each color channel
    for i in range(3):
        score, diff = ssim(img_reference[:, :, i], img_comparison[:, :, i], full=True)
        ssim_scores.append(score)
    # Calculate the mean SSIM score
    mean_ssim = np.mean(ssim_scores)
    # Convert the diff image to uint8 (make it useful for visualization)
    diff = (diff * 255).astype("uint8")
    return mean_ssim, diff


if __name__ == "__main__":
    main()