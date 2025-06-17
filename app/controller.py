import time
import threading
import subprocess
import numpy as np
from dataclasses import dataclass
import os
from app.img_handler import (
    load_img,
    cv2_to_base64,

    calculate_similarity,
    calculate_similarity_diff,

    process_difference_refined,
    process_difference_rgb,
)
from app.coollab_handler import (
    open_coollab_project,
)

def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        try:
            with open(file_path, "x") as file:
                pass
        except Exception as e:
            print(f"Error occurred while creating file : {e}")
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error : '{file_path}' not found")
    except Exception as e:
        print(f"Error while reading file : {e}")

def write_file(file_path: str, content: str):
    try:
        with open(file_path, "w") as file:
            file.write(content.strip())
    except FileNotFoundError:
        print(f"Error : '{file_path}' not found")
    except Exception as e:
        print(f"Error while writing on file : {e}")

@dataclass
class TestData:
    id: int
    name: str
    score: float = 0.0
    status: bool = False
    img_ref: str = ""
    img_comp: str = ""
    results: dict = None

    def __post_init__(self):
        if self.results is None:
            self.results = {}

class Controller:

    def __init__(self, page):
        self.page = page
        self.test_panel = None
        self.preview_panel = None
        self.coollab_path = None
        self.current_test_count = 0
        self.is_focused = False
        self.tests = [
            TestData(1, "Test 1", img_ref="test1_o.png", img_comp="test1_e.png"),
            TestData(2, "Test 2", img_ref="test2_o.png", img_comp="test2_e.png"),
            TestData(3, "Test 3", img_ref="test3_o.png", img_comp="test3_e.png"),
            TestData(4, "Test 4", img_ref="test4_o.png", img_comp="test4_e.png"),
            TestData(5, "Test 5", img_ref="test5_o.jpeg", img_comp="test5_e.jpeg"),
        ]
    
    def set_focus_state(self, focus_state: bool = False):
        self.is_focused = focus_state
        print(self.is_focused)

    def set_coollab_path(self, coollab_path: str):
        self.coollab_path = coollab_path
        cache_path = read_file('coollab_path_cache.txt')
        if coollab_path != cache_path:
            write_file('coollab_path_cache.txt', coollab_path)
    
    def get_coollab_path(self) -> str:
        if self.coollab_path:
            return self.coollab_path
        else:
            self.coollab_path = read_file('coollab_path_cache.txt') if read_file('coollab_path_cache.txt') != "" else ""
            return self.coollab_path

# --------------------------------------
# UI Controller Methods
# --------------------------------------

    def set_preview_panel(self, panel):
        self.preview_panel = panel

    def set_test_panel(self, panel):
        self.test_panel = panel

    def update_preview(self, test_id: int, filter: str):
        if self.preview_panel:
            for test_data in self.tests:
                if test_data.id == test_id:
                    display_text = test_data.name

                    if filter == "threshold":
                        display_img = test_data.results["thresh"]
                    elif filter == "original":
                        display_img = load_img(test_data.img_ref)
                    elif filter == "exported":
                        display_img = load_img(test_data.img_comp)
                    else:
                        display_img = test_data.results["outlined"]

                    self.preview_panel.image_section.update_img(cv2_to_base64(display_img))
                    break
                else:
                    display_text = "No test found"

            self.preview_panel.update_content(display_text)
            self.preview_panel.filter_section.selected_test_id = test_id
            self.preview_panel.update()

# --------------------------------------
# Test Controller Methods
# --------------------------------------

# ------ UI

    def reset_tests(self):
        for test in self.tests:
            test.score = 0.0
            test.status = False
            test.results = None

    def initialize_ui_for_tests(self, total_pending: int):
        self.reset_tests()
        self.test_panel.start_test(total_pending)

        self.test_panel.version_section.update()
        self.test_panel.counter_section.update()

    def update_progress_bar(self, total_pending:int):
        progress_value = (1 / total_pending)*self.current_test_count if total_pending > 0 and self.current_test_count > 0 else 0
        self.test_panel.version_section.update_progress(progress_value)
        self.test_panel.version_section.update()

    def update_single_test_result(self, tid, s, st):
        self.test_panel.project_section.replace_tile(tid, s, st)
        self.test_panel.counter_section.increment_current()
        self.test_panel.update()
    
    def finalize_ui(self):
        self.test_panel.version_section.enable_controls()
        self.test_panel.version_section.update_progress(1)

        self.test_panel.version_section.update()
    
    def reset_ui_on_relaunch(self, test_data: TestData):
        # Reset the preview panel if it was the selected test
        if self.preview_panel.filter_section.selected_test_id == test_data.id:
            self.preview_panel.filter_section.selected_test_id = None
            self.preview_panel.image_section.reset()
            self.preview_panel.update()
        # Reset test panel
        self.test_panel.project_section.replace_tile(test_data.id, 0, False)
        self.current_test_count -= 1
        self.update_progress_bar(len(self.tests))
        self.test_panel.counter_section.decrement_current()
        test_data.score = 0.0
        test_data.status = False
        test_data.results = None

        self.test_panel.update()

# ------ Test Processing

    def relaunch_test(self, test_id: int):

        for test_data in self.tests:
            if test_data.id == test_id:
                self.reset_ui_on_relaunch(test_data)

                test_result = self.process_test(test_data)
                if test_result is not None:
                    test_data.score = test_result["score"]
                    test_data.status = True
                    test_data.results = test_result["results"]
                self.current_test_count += 1
                self.update_progress_bar(len(self.tests))
                self.update_single_test_result(test_id, test_data.score, test_data.status)
                break
        self.test_panel.update()

    def process_test(self, test_data: TestData) -> dict[dict, float]:
        # Launch coollab with the provided path and get the exported images
        img_comparison = load_img(test_data.img_comp)
        img_reference = load_img(test_data.img_ref)
        score, diff = calculate_similarity(img_reference, img_comparison)
        result_diff = process_difference_refined(diff, img_reference, img_comparison)
        score = -np.log10(score)*10000
        return {
            'results': result_diff,
            'score': score,
        }

# ---------- Launch Test Whole Method ----------

    def launch_test(self, coollab_path:str):
        # coollab_path= "C:/Users/elvin/AppData/Roaming/Coollab Launcher/Installed Versions/1.2.0 MacOS/Coollab.exe"
        # open_coollab_project(coollab_path, "C:/Users/elvin/AppData/Roaming/Coollab Launcher/Projects/Test.coollab")
        self.set_coollab_path(coollab_path)
        if self.preview_panel:
            self.preview_panel.start_test()
            self.preview_panel.update()
        if self.test_panel:
            total_pending = len(self.tests)

            self.initialize_ui_for_tests(total_pending)

            self.current_test_count = 0
            for test_data in self.tests:
                self.current_test_count += 1
                test_id = test_data.id

                self.test_panel.project_section.add_processing_tile(test_id)
                self.test_panel.project_section.update()

                # Process
                # time.sleep(0.5)
                test_result = self.process_test(test_data)
                if test_result is not None:
                    test_data.score = test_result["score"]
                    test_data.status = True
                    test_data.results = test_result["results"]

                # self.page.run_thread(lambda tid=test_id, s=score, st=status: self.update_single_test_result(self.current_test_count, total_pending, tid, s, st))
                self.update_progress_bar(total_pending)
                self.update_single_test_result(test_id, test_data.score, test_data.status)

            self.finalize_ui()
