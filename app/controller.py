import numpy as np
from dataclasses import dataclass
from time import sleep
from pathlib import Path
from slugify import slugify
from services.coollab_handler import start_coollab
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
from pynput.mouse import Controller as MouseController

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
        self.mouse = MouseController()

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
    
    def _update_progress_bar(self, direction: int):
        if len(self.tests) == 0:
            return
        step = 1 / len(self.tests)
        current_value = self.test_panel.progress_bar.value or 0
        new_value = current_value + direction * step
        clamped_value = max(0.005, min(1, new_value))
        self.test_panel.update_progress(clamped_value)
    
    def increment_progress_bar(self):
        self._update_progress_bar(+1)

    def decrement_progress_bar(self):
        self._update_progress_bar(-1)
    
    def reset_ui_on_relaunch(self, test_data: TestData):
    # Reset the preview panel if it was the selected test
        if self.image_panel.filter_section.selected_test_id == test_data.id:
            self.image_panel.filter_section.reset()
            self.image_panel.image_section.reset()
    # Reset progression
        self.decrement_progress_bar()
        self.test_panel.counter_section.decrement_current()

    def reset_all_test_tiles(self):
        if self.test_panel:
            for test_data in self.tests:
                test_data.reset()
                test_data.status = TestStatus.IN_PROGRESS
                self.test_panel.project_section.update_tile(test_data)
    def update_all_test_tiles(self):
        if  self.test_panel:
            for test_data in self.tests:
                self.test_panel.project_section.update_tile(test_data)
    def init_test_tiles(self):
        if  self.test_panel:
            self.test_panel.project_section.clear_test_view()
            self.update_all_test_tiles()

# --------------------------------------
# Coollab
# --------------------------------------

    async def try_start_coollab(self, path: str):
        if not path:
            return False
        try:
            await asyncio.to_thread(start_coollab, Path(path))
            sleep(1)
            self.coollab = Coollab()
            return True
        except Exception as e:
            print(f"[ERROR] Error on Coollab launch: {e}")
            return False
    
    async def relaunch_coollab(self, path: str):
        if self.coollab:
            self.coollab.close_app()
            self.coollab = None
        await self.try_start_coollab(path)

# --------------------------------------
# Tests
# --------------------------------------

    async def check_tests_validity(self):
        if self.test_panel:
            self.test_panel.counter_section.update_size(len(self.tests))
            self.test_panel.path_section.disable_controls()
            self.test_panel.update_progress(0.005)

        self.coollab.on_image_export_finished(self.update_status_on_export_finished)
        for test_data in self.tests:
            if not ref_file_exist(test_data):
                self.export_queue_num += 1
                print("[INFO] Reference image for test '", test_data.name, "' does not exist.")
                await self.launch_export(self.coollab, test_data, "ref")
            else:
                test_data.status = TestStatus.READY
                # if self.test_panel:
                #     # self.test_panel.project_section.update_tile(test_data)
                #     self.increment_progress_bar()
            
        while self.export_queue_num > 0:
            print("[WAITING] Waiting for queue to be empty")
            await asyncio.sleep(0.5)
        if self.test_panel: 
            self.test_panel.path_section.enable_controls()
    
    async def launch_all_tests(self):
        if self.export_queue_num > 0:
            print("[INFO] Export queue not finished")
            return

        if self.image_panel:
            self.image_panel.reset()
        if self.test_panel:
            self.test_panel.path_section.disable_controls()
            self.test_panel.update_progress(0.005)
            self.test_panel.counter_section.reset_current()

            self.reset_all_test_tiles()
            
            self.coollab.on_image_export_finished(self.process_test_on_export_finished)
            for test_data in self.tests:
                self.export_queue_num += 1
                await self.launch_export(self.coollab, test_data, "exp")

            while self.export_queue_num > 0:
                print(f"[WAITING] Waiting for queue to be empty. Current num : {self.export_queue_num}")
                await asyncio.sleep(0.5)
            if self.test_panel:
                self.test_panel.path_section.enable_controls()
                self.test_panel.update_progress(1)

    async def relaunch_test(self, test_id: int):
        self.coollab.on_image_export_finished(self.process_test_on_export_finished)
        for test_data in self.tests:
            if test_data.id == test_id:
                print("[INFO] Relaunching test :", test_data.name)
                self.reset_ui_on_relaunch(test_data)
                test_data.reset()
                test_data.status = TestStatus.IN_PROGRESS
                self.test_panel.project_section.update_tile(test_data)
                self.export_queue_num += 1
                await self.launch_export(self.coollab, test_data, "exp")
                break

    async def update_all_tests_ref(self):
        if self.export_queue_num > 0:
            print("[INFO] Export queue not finished")
            return

        if self.image_panel:
            self.image_panel.reset()
        if self.test_panel:
            self.test_panel.path_section.disable_controls()
            self.test_panel.update_progress(0.005)

            self.reset_all_test_tiles()
            
            self.coollab.on_image_export_finished(self.update_status_on_export_finished)
            for test_data in self.tests:
                self.export_queue_num += 1
                await self.launch_export(self.coollab, test_data, "ref")

            while self.export_queue_num > 0:
                print(f"[WAITING] Waiting for queue to be empty. Current num : {self.export_queue_num}")
                await asyncio.sleep(0.5)
            if self.test_panel:
                self.test_panel.path_section.enable_controls()
                self.test_panel.update_progress(1)
            
    async def update_test_ref(self, test_id: int):
        self.coollab.on_image_export_finished(self.update_status_on_export_finished)
        for test_data in self.tests:
            if test_data.id == test_id:
                print("[INFO] Reinitializing test ref :", test_data.name)
                self.reset_ui_on_relaunch(test_data)
                test_data.reset()
                test_data.status = TestStatus.IN_PROGRESS
                self.test_panel.project_section.update_tile(test_data)
                self.export_queue_num += 1
                await self.launch_export(self.coollab, test_data, "ref")
                break

# # --------------------------------------
# # Utils methods
# # --------------------------------------

    async def launch_export(self, 
                            coollab: Coollab, 
                            test_data: TestData, 
                            folder: str | None  = None,
                            height: int | None = None,
                            width: int | None = None
    ):
        project_path = test_data.get_project_file_path()
        folder_path = (Path("assets/img") if folder is None else Path("assets/img") / folder).resolve()

        img_reference = load_img(test_data.get_ref_file_path())
        if img_reference is not None:
            if height is None:
                height = img_reference.shape[0]
            if width is None:
                width = img_reference.shape[1]
        
        if project_path.exists():
            await coollab.open_project(str(project_path))
            await coollab.start_image_export(
                width,
                height,
                folder= str(folder_path.resolve()),
                filename=test_data.name,
                extension=None,
                project_autosave=False,
                export_file_overwrite=True,
            )
        
    def find_test_from_file_path(self, absolute_path: str) -> TestData | None:
        filename = Path(absolute_path).stem
        for test_data in self.tests:
            if test_data.name == filename:
                return test_data
        return None
    
    def update_status_on_export_finished(self, exported_path: str):
        # print(f"[DEBUG] Exported image message recieved on : {exported_path}")
        test_data = self.find_test_from_file_path(exported_path)
        if not test_data:
            print(f"[ERROR] Test data not found for exported path: {exported_path}")
            return
        
        test_data.status = TestStatus.READY

        if self.test_panel:
            self.test_panel.project_section.update_tile(test_data)
            # self.increment_progress_bar()
        self.export_queue_num -= 1

    def process_test_on_export_finished(self, exported_path: str):
        test_data = self.find_test_from_file_path(exported_path)
        if not test_data:
            print(f"[ERROR] Test data not found for exported path: {exported_path}")
            return
        
        test_data.exported_img_path = exported_path
        img_reference = load_img(test_data.get_ref_file_path())
        img_comparison = load_img(exported_path)

        # --- Test logic ---
        score, diff = calculate_similarity(img_reference, img_comparison)
        result_diff = process_difference_refined(diff, img_reference, img_comparison)
        score = max(0.0, -np.log10(score)*10000)

        result_diff["ref"] = img_reference
        result_diff["exp"] = img_comparison
        test_data.score = score
        test_data.results = result_diff
        test_data.status = TestStatus.PASSED if score <= good_score_threshold else TestStatus.FAILED
        
        if self.test_panel:
            self.test_panel.project_section.update_tile(test_data)
            self.increment_progress_bar()
            self.test_panel.counter_section.increment_current()
        self.export_queue_num -= 1

