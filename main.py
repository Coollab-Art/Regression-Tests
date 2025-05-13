import os
import sys
import time
import random
from compute_img import (
    load_img,
    calculate_similarity,
    calculate_similarity_2,
    process_difference,
    process_difference_2,
    process_difference_3,
    show_all_diff,
    show_mask,
    show_outlined,
)

def main() -> None:
    img_comparison = load_img('chess-altered-mid.png')
    img_reference = load_img('chess.png')

    score, diff = calculate_similarity(img_reference, img_comparison)
    result_diff = process_difference_2(diff, img_reference, img_comparison)
    # score, diff = calculate_similarity_2(img_reference, img_comparison)
    # result_diff = process_difference_3(diff, img_reference, img_comparison)
    print("Average SSIM:", score)
    # print("Average SSIM:", score)
    # print("Similarity Score: {:.5f}%".format(score * 100))
    show_outlined(result_diff)
    # show_outlined(result_diff, img_reference)
    # show_all_diff(result_diff, img_reference, img_comparison)

if __name__ == "__main__":
    main()