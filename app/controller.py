import numpy as np
from dataclasses import dataclass
from time import sleep
from pathlib import Path
from slugify import slugify
import asyncio
from services.img_handler import (
    load_img,
    cv2_to_base64,
    calculate_similarity,
    process_difference_refined,
)
from services.Coollab import Coollab
from TestsData import TestData, get_test_data, TestStatus
from services.utils import (
    read_file,
    write_file,
    ref_file_exist,
)
from services.ImageType import ImageType

# coollab_path= "C:/Users/elvin/AppData/Roaming/Coollab Launcher/Installed Versions/1.2.0 MacOS/Coollab.exe"
good_score_threshold = 200

# --------------------------------------
# Controller Class
# --------------------------------------

class Controller:

    def __init__(self, page):
        self.page = page
        self.test_panel = None
        self.image_panel = None
        self.coollab_path = None
        self.is_focused: bool = False
        self.coollab: Coollab = None
        self.export_queue_num: int = 0
        self.tests = get_test_data()

        self.waiting_for_export:  bool = False

# --------------------------------------
# Setters and Getters
# --------------------------------------
    
    def set_image_panel(self, panel):
        self.image_panel = panel

    def set_test_panel(self, panel):
        self.test_panel = panel
    
    def set_coollab_path(self, coollab_path: str):
        self.coollab_path = coollab_path
        cache_path = read_file('coollab_path_cache.txt')
        if coollab_path != cache_path:
            write_file('coollab_path_cache.txt', coollab_path)
    
    def get_coollab_path(self) -> str:
        if self.coollab_path:
            return self.coollab_path
        else:
            cache_path = read_file('coollab_path_cache.txt')
            self.coollab_path = cache_path if cache_path != "" else ""
            return self.coollab_path
        
    def set_focus_state(self, focus_state: bool = False):
        self.is_focused = focus_state

# --------------------------------------
# UI
# --------------------------------------

    def reset_img_filter(self):
        if self.image_panel:
            self.image_panel.filter_section.reset()
    
    def update_img_display(self, test_id: int, filter: ImageType):
        if self.image_panel:
            for test_data in self.tests:
                if test_data.id == test_id:
                    if filter == ImageType.THRESHOLD:
                        display_img = test_data.results["thresh"]
                    elif filter == ImageType.ORIGINAL:
                        display_img = test_data.results["ref"]
                    elif filter == ImageType.EXPORTED:
                        display_img = test_data.results["exp"]
                    else:
                        display_img = test_data.results["outlined"]

                    self.image_panel.image_section.update_img(cv2_to_base64(display_img))
                    break

            self.image_panel.filter_section.selected_test_id = test_id
    
    def increment_progress_bar(self):
        progress_value = self.test_panel.path_section.progress_bar.value + ((1 / len(self.tests)) if len(self.tests) > 0 else 0)
        self.test_panel.path_section.update_progress(progress_value)
    def decrement_progress_bar(self):
        progress_value = self.test_panel.path_section.progress_bar.value - ((1 / len(self.tests)) if len(self.tests) > 0 else 0)
        self.test_panel.path_section.update_progress(progress_value)
    
    def reset_ui_on_relaunch(self, test_data: TestData):
    # Reset the preview panel if it was the selected test
        if self.image_panel.filter_section.selected_test_id == test_data.id:
            self.image_panel.filter_section.reset()
            self.image_panel.image_section.reset()
    # Reset progresion
        self.decrement_progress_bar()
        self.test_panel.counter_section.decrement_current()

# --------------------------------------
# Tests
# --------------------------------------

    async def check_tests_validity(self):
        if self.test_panel:
            self.test_panel.counter_section.update_size(len(self.tests))
            self.test_panel.path_section.disable_controls()
            self.test_panel.update_progress(0)

        self.coollab.on_image_export_finished(self.update_status_on_export_finished)
        for test_data in self.tests:
            if not ref_file_exist(test_data):
                self.export_queue_num += 1
                print("Reference image for test", test_data.name, "does not exist. Export...")
                self.launch_export(self.coollab, test_data, "ref")
            else:
                test_data.status = TestStatus.READY
                if self.test_panel:
                    self.test_panel.project_section.replace_tile(test_data)
                    self.increment_progress_bar()
            
        while self.export_queue_num > 0:
            await asyncio.sleep(0.5)
        if self.test_panel: 
            self.test_panel.path_section.enable_controls()
    
    async def launch_all_tests(self):
        # TODO if change coollab path and if export queue is not empty
        if self.image_panel:
            self.image_panel.reset()
        if self.test_panel:
            self.test_panel.path_section.disable_controls()
            self.test_panel.update_progress(0)
            
            self.coollab.on_image_export_finished(self.process_test_on_export_finished)
            for test_data in self.tests:
                test_data.reset()
                self.test_panel.project_section.replace_tile(test_data)
                self.export_queue_num += 1
                self.launch_export(self.coollab, test_data, "exp")

            while self.export_queue_num > 0:
                await asyncio.sleep(0.5)
            if self.test_panel:
                self.test_panel.path_section.enable_controls()
                self.test_panel.update_progress(1)

    async def relaunch_test(self, test_id: int):
        self.coollab.on_image_export_finished(self.process_test_on_export_finished)
        for test_data in self.tests:
            if test_data.id == test_id:
                print("Relaunching test :", test_data.name)
                self.reset_ui_on_relaunch(test_data)
                test_data.reset()
                self.test_panel.project_section.replace_tile(test_data)
                self.export_queue_num += 1
                self.launch_export(self.coollab, test_data, "exp")
                break

# # --------------------------------------
# # Utils methods
# # --------------------------------------

    async def launch_export(self, coollab: Coollab, test_data: TestData, folder: str, height: int | None = None, width: int | None = None):
        project_path = Path(test_data.get_project_file_path).resolve()
        folder_path = Path("assets/img") if folder is None else Path("assets/img") / folder
        if project_path.exists():
            print("Opening project")
            await coollab.open_project(str(project_path))
            await coollab.start_image_export(
                width,
                height,
                folder= folder_path.resolve(),
                filename=test_data.name,
                extension=None, # TODO coté coollab detect si None passe bien
                export_file_overwrite=True,
            )
        
    def find_test_from_file_path(self, absolute_path: str) -> TestData | None:
        filename = Path(absolute_path).stem
        for test_data in self.tests:
            if test_data.name == filename:
                return test_data
        return None
    
    def update_status_on_export_finished(self, exported_path: str):
        test_data = self.find_test_from_file_path(exported_path)
        if not test_data:
            print(f"Error: Test data not found for exported path: {exported_path}")
            return
        
        test_data.status = TestStatus.READY

        if self.test_panel:
            self.test_panel.project_section.replace_tile(test_data)
            self.increment_progress_bar()
        self.export_queue_num -= 1

    def process_test_on_export_finished(self, exported_path: str):
        test_data = self.find_test_from_file_path(exported_path)
        if not test_data:
            print(f"Error: Test data not found for exported path: {exported_path}")
            return
        
        test_data.exported_img_path = exported_path
        img_reference = load_img(test_data.get_ref_file_path())
        img_comparison = load_img(exported_path)

        # --- Test logic ---
        score, diff = calculate_similarity(img_reference, img_comparison)
        result_diff = process_difference_refined(diff, img_reference, img_comparison)
        score = -np.log10(score)*10000

        result_diff["ref"] = img_reference
        result_diff["exp"] = img_comparison
        test_data.score = score
        test_data.results = result_diff
        test_data.status = TestStatus.PASSED if score <= good_score_threshold else TestStatus.FAILED
        
        if self.test_panel:
            self.test_panel.project_section.replace_tile(test_data)
            self.increment_progress_bar()
            self.test_panel.counter_section.increment_current()
        self.export_queue_num -= 1

