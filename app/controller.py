import numpy as np
from dataclasses import dataclass
from time import sleep
from pathlib import Path
from slugify import slugify
import asyncio
from services.img_handler import (
    load_img_from_assets,
    img_name_with_extension,
    cv2_to_base64,

    calculate_similarity,
    calculate_similarity_diff,

    process_difference_refined,
    process_difference_rgb,
)
from services.Coollab import Coollab
from TestsData import TestData, get_test_data
from services.utils import (
    read_file,
    write_file,
    ref_file_exist,
)
from services.ImageType import ImageType

# coollab_path= "C:/Users/elvin/AppData/Roaming/Coollab Launcher/Installed Versions/1.2.0 MacOS/Coollab.exe"

# --------------------------------------
# Controller Class
# --------------------------------------

class Controller:

    def __init__(self, page):
        self.page = page
        self.test_panel = None
        self.image_panel = None
        self.coollab_path = None
        self.is_focused = False

        self.current_test_count = 0
        self.waiting_for_export = False
        self.tests = get_test_data()

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

# --------------------------------------
# Tests
# --------------------------------------

    def check_tests_validity(self) -> bool:
        for test_data in self.tests:
            if not ref_file_exist(test_data):
                print("Ref not exist")
                self.launch_export(self.coollab, test_data, "ref")
        return True
    
    def launch_all_tests(self):
        # self.coollab.on_image_export_finished(self.pursue)
        if self.image_panel:
            self.image_panel.reset()
        if self.test_panel:
            self.reset_tests()
            total_pending = len(self.tests)
            self.test_panel.init_test(total_pending)

            # self.current_test_count = 0
            # for test_data in self.tests:
            #     self.current_test_count += 1

            #     self.test_panel.project_section.add_processing_tile(test_data)

            #     test_result = self.process_test(test_data, self.coollab)
            #     if test_result is not None:
            #         test_data.score = test_result["score"]
            #         test_data.status = True
            #         test_data.results = test_result["results"]

            #     # self.page.run_thread(lambda tid=test_id, s=score, st=status: self.update_single_test_result(self.current_test_count, total_pending, tid, s, st))
            #     self.update_progress_bar(total_pending)
            #     self.update_single_test_result(test_data)

            # self.finalize_ui()

    def relaunch_test(self, test_id: int):
        print("Relaunching test :", test_id)

    def reset_tests(self):
        for test in self.tests:
            test.score = 0.0
            test.status = False
            test.results = None

# # --------------------------------------
# # Utils methods
# # --------------------------------------

    async def launch_export(self, coollab: Coollab, test_data: TestData, folder: str, height: int | None = None, width: int | None = None):
        project_path = Path(test_data.get_project_file_path)
        folder_path = Path("assets/img") if folder is None else Path("assets/img") / folder
        if project_path.exists():
            print("Opening project")
            await coollab.open_project(str(project_path))
            await coollab.start_image_export(
                width,
                height,
                folder= folder_path.resolve(),
                filename=test_data.get_name(),
                extension=test_data.img_export_extension,
                export_file_overwrite=True,
            )






    
#     def pursue(self):
#         self.waiting_for_export = False

# # --------------------------------------
# # UI Controller Methods
# # --------------------------------------

# # load_img_from_assets(img_name_with_extension(img_name), "ref")
# # load_img_from_assets(img_name_with_extension(img_name, test_data.img_export_extension), "exp")
# # --------------------------------------
# # Test Controller Methods
# # --------------------------------------

# # ------ UI

#     def reset_tests(self):
#         for test in self.tests:
#             test.score = 0.0
#             test.status = False
#             test.results = None

#     def update_progress_bar(self, total_pending:int):
#         progress_value = (1 / total_pending)*self.current_test_count if total_pending > 0 and self.current_test_count > 0 else 0
#         self.test_panel.path_section.update_progress(progress_value)
#         self.test_panel.path_section.update()

#     def update_single_test_result(self, test_data: TestData):
#         self.test_panel.project_section.replace_tile(test_data)
#         self.test_panel.counter_section.increment_current()
#         self.test_panel.update()
    
#     def finalize_ui(self):
#         self.test_panel.path_section.enable_controls()
#         self.test_panel.path_section.update_progress(1)

#         self.test_panel.path_section.update()
    
#     def reset_ui_on_relaunch(self, test_data: TestData):
#     # Reset the preview panel if it was the selected test
#         if self.image_panel.filter_section.selected_test_id == test_data.id:
#             self.image_panel.filter_section.reset()
#             self.image_panel.image_section.reset()
#             self.image_panel.update()
#     # Reset test panel
#         self.test_panel.project_section.replace_tile(test_data)
#         self.current_test_count -= 1
#         self.update_progress_bar(len(self.tests))
#         self.test_panel.counter_section.decrement_current()
#         test_data.score = 0.0
#         test_data.status = False
#         test_data.results = None

#         self.test_panel.update()

# # ------ Redo test
#     def relaunch_test(self, test_id: int):
#         start_coollab(Path(self.get_coollab_path()))
#         with Coollab() as coollab:
#             coollab.on_image_export_finished(self.pursue)
#             for test_data in self.tests:
#                 if test_data.id == test_id:
#                     test_data.reset()
#                     self.reset_ui_on_relaunch(test_data)
#                     print(f"Relaunching test: {test_data.name}")
#                     test_result = self.process_test(test_data, coollab)
#                     if test_result is not None:
#                         test_data.score = test_result["score"]
#                         test_data.status = True
#                         test_data.results = test_result["results"]
#                     self.current_test_count += 1
#                     self.update_progress_bar(len(self.tests))
#                     self.update_single_test_result(test_data)
#                     break
#             self.test_panel.update()
#             coollab.close_app()

# # ---------- Launch all tests ----------
#     def launch_test(self, coollab_path:str):
#         # coollab_path= "C:/Users/elvin/AppData/Roaming/Coollab Launcher/Installed Versions/1.2.0 MacOS/Coollab.exe"
        
#         self.set_coollab_path(coollab_path)
#         start_coollab(Path(self.get_coollab_path()))
#         with Coollab() as coollab:
#             coollab.on_image_export_finished(self.pursue)
#             if self.image_panel:
#                 self.image_panel.start_test()
#                 self.image_panel.update()
#             if self.test_panel:
#                 total_pending = len(self.tests)

#                 self.initialize_ui_for_tests(total_pending)

#                 self.current_test_count = 0
#                 for test_data in self.tests:
#                     self.current_test_count += 1
#                     test_id = test_data.id

#                     self.test_panel.project_section.add_processing_tile(test_data)
#                     self.test_panel.project_section.update()

#                     test_result = self.process_test(test_data, coollab)
#                     if test_result is not None:
#                         test_data.score = test_result["score"]
#                         test_data.status = True
#                         test_data.results = test_result["results"]

#                     # self.page.run_thread(lambda tid=test_id, s=score, st=status: self.update_single_test_result(self.current_test_count, total_pending, tid, s, st))
#                     self.update_progress_bar(total_pending)
#                     self.update_single_test_result(test_data)

#                 self.finalize_ui()
#                 coollab.close_app()

#     def process_test(self, test_data: TestData, coollab: Coollab) -> dict[dict, float]:

#     # --- Load img reference ---
#         img_name = slugify(test_data.name)
#         img_reference = load_img_from_assets(img_name_with_extension(img_name), "ref")

#     # --- Export img ---
#         project_path = Path().resolve() / "assets" / "projects" / str(test_data.name+".coollab")
#         if project_path.exists():
#             print("Opening project")
#             coollab.open_project(str(project_path))
#             sleep(2)  # Wait for project to load
#             self.waiting_for_export = True
#             coollab.export_image(folder=self.export_folder_path, filename=img_name, height=img_reference.shape[0], width=img_reference.shape[1], extension=test_data.img_export_extension)
#             while( self.waiting_for_export ):
#                 print("Waiting for image export to finish...")
#                 sleep(0.3)
                
#     # --- Load exported img ---
#         img_comparison = load_img_from_assets(img_name_with_extension(img_name, test_data.img_export_extension), "exp")

#     # --- Test logic ---
#         score, diff = calculate_similarity(img_reference, img_comparison)
#         result_diff = process_difference_refined(diff, img_reference, img_comparison)
#         score = -np.log10(score)*10000
#         return {
#             'results': result_diff,
#             'score': score,
#         }
    

# # --------------------------------------
# # Reference images Controller Methods
# # --------------------------------------