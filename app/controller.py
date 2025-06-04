import time
import threading
from img_handler import (
    load_img,
    cv2_to_base64,

    calculate_similarity,
    calculate_similarity_diff,

    process_difference_refined,
    process_difference_rgb,
)

class Controller:

    def __init__(self, page):
        self.page = page
        self.test_panel = None
        self.preview_panel = None
        self.tests = [
            {"id": 1, "name": "Test 1", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
            {"id": 2, "name": "Test 2", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
            {"id": 3, "name": "Test 3", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
            {"id": 4, "name": "Test 4", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
            {"id": 5, "name": "Test 5", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
            {"id": 6, "name": "Test 6", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
            {"id": 7, "name": "Test 7", "score": 0, "status": False, "img_ref": "chess.png", "img_comp": "chess-altered-hard.png"},
        ]

# --------------------------------------
# UI Controller Methods
# --------------------------------------

    def set_preview_panel(self, panel):
        self.preview_panel = panel

    def set_test_panel(self, panel):
        self.test_panel = panel

    def update_preview(self, test_id: int):
        if self.preview_panel:
            for test_data in self.tests:
                if test_data["id"] == test_id:
                    original_img = load_img(test_data["img_ref"])
                    exported_img = load_img(test_data["img_comp"])
                    display_text = test_data["name"]

                    filter = self.preview_panel.selector_section.get_filter()
                    # filter = None
                    if filter == "threshold":
                        display_img = test_data["results"]["thresh"]
                    elif filter == "original":
                        display_img = original_img
                    elif filter == "exported":
                        display_img = exported_img
                    else:
                        display_img = test_data["results"]["outlined"]

                    self.preview_panel.comparison_section.update_img(cv2_to_base64(original_img), cv2_to_base64(exported_img))
                    self.preview_panel.image_section.update_img(cv2_to_base64(display_img))
                    break
                else:
                    display_text = "No test found"

            self.preview_panel.update_content(display_text)
            self.preview_panel.selector_section.set_selected(test_id)
            self.preview_panel.update()

# Test Launching Method
    def reset_tests(self):
        for test in self.tests:
            test["score"] = 0
            test["status"] = False
            test["results"] = None

    def initialize_ui_for_tests(self, total_pending: int):
        self.reset_tests()
        self.test_panel.start_test(total_pending)

        self.test_panel.version_section.update()
        self.test_panel.counter_section.update()

    def update_single_test_result(self, current_test_count: int, total_pending:int, tid, s, st):
        progress_value = (1 / total_pending)*current_test_count if total_pending > 0 and current_test_count > 0 else 0
        self.test_panel.update_result(progress_value, tid, s, st)

        self.test_panel.update()
    
    def process_test(self, coollab_path: str, test_data: dict) -> dict[dict, float]:
        # Launch coollab with the provided path and get the exported images
        img_comparison = load_img(test_data["img_comp"])
        img_reference = load_img(test_data["img_ref"])
        score, diff = calculate_similarity(img_reference, img_comparison)
        result_diff = process_difference_refined(diff, img_reference, img_comparison)
        return {
            'results': result_diff,
            'score': score,
        }
    
    def finalize_ui(self):
        self.test_panel.end_test()

        self.test_panel.version_section.update()

    def launch_test(self, coollab_path:str):
        if self.preview_panel:
            self.preview_panel.start_test()
            self.preview_panel.update()
        if self.test_panel:
            total_pending = len(self.tests)

            self.initialize_ui_for_tests(total_pending)

            current_test_count = 0
            for test_data in self.tests:
                current_test_count += 1
                test_id = test_data["id"]

                self.test_panel.add_pending_project(test_id)
                self.test_panel.project_section.update()

                # Process
                # time.sleep(0.5)
                test_result = self.process_test(coollab_path, test_data)
                if test_result is not None:
                    test_data["score"] = test_result["score"]
                    test_data["status"] = True
                    test_data["results"] = test_result["results"]

                # self.page.run_thread(lambda tid=test_id, s=score, st=status: self.update_single_test_result(current_test_count, total_pending, tid, s, st))
                self.update_single_test_result(current_test_count, total_pending, test_id, test_data["score"], test_data["status"])

            self.finalize_ui()
