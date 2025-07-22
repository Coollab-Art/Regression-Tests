import os
import sys
import time
import random
import subprocess
import time
# from img_handler import (
#     load_img,

#     calculate_similarity,
#     calculate_similarity_diff,

#     process_difference,
#     process_difference_refined,
#     process_difference_rgb,

#     show_all_diff,
#     show_diff,
#     show_mask,
#     show_outlined,
#     show_test,
# )

def main() -> None:
    # img_comparison = load_img_from_assets('chess-altered-hard.png')
    # img_reference = load_img_from_assets('chess.png')

    # score, diff = calculate_similarity(img_reference, img_comparison)
    # result_diff = process_difference_refined(diff, img_reference, img_comparison)
    # score, diff = calculate_similarity_diff(img_reference, img_comparison)
    # result_diff = process_difference_3(diff, img_reference, img_comparison)

    # print("Average SSIM:", score)
    # print("Similarity Score: {:.5f}%".format(score * 100))

    # show_outlined(result_diff)
    # show_diff(result_diff)
    # show_outlined(result_diff, img_reference)
    # show_all_diff(result_diff, img_reference, img_comparison)

    # show_test(result_diff, img_reference, img_comparison)

    process = subprocess.Popen(['C:/Users/elvin/AppData/Roaming/Coollab Launcher/Installed Versions/1.2.0 MacOS/Coollab.exe', '--open_project', 'C:/Users/elvin/AppData/Roaming/Coollab Launcher/Projects/Test.coollab'])
    # process = subprocess.Popen(['C:/Users/elvin/AppData/Roaming/"Coollab Launcher"/"Installed Versions"/"1.2.0 MacOS"/Coollab.exe'])
    # time.sleep(5)
    # process.terminate()

main()