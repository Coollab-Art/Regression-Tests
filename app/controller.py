import time
import threading

class Controller:

    def __init__(self, page):
        self.page = page
        self.test_panel = None
        self.preview_panel = None
        self.tests = [
            {"id": 1, "name": "Test 1", "score": 87.5},
            {"id": 2, "name": "Test 2", "score": 55.5},
            {"id": 3, "name": "Test 3", "score": 90.5},
            {"id": 4, "name": "Test 4", "score": 53.5},
            {"id": 5, "name": "Test 5", "score": 50.5},
            {"id": 6, "name": "Test 6", "score": 90.5},
            {"id": 7, "name": "Test 7", "score": 00.0},
        ]

# --------------------------------------
# UI Controller Methods
# --------------------------------------

    def set_preview_panel(self, panel):
        self.preview_panel = panel

    def set_test_panel(self, panel):
        self.test_panel = panel

    def update_preview(self, test_id: int):
        result = f"Image test {test_id}"
        # print(f"[Controller] Switch image: Test {test_id} → {result}")

        if self.preview_panel:
            self.preview_panel.update_content(result)
            self.preview_panel.image_section.update()

# Test Launching Method
    def initialize_ui_for_tests(self, total_pending: int):
        self.test_panel.start_test(total_pending)

        self.test_panel.version_section.update()
        self.test_panel.counter_section.update()

    def update_single_test_result(self, current_test_count: int, total_pending:int, tid, s, st):
        progress_value = (1 / total_pending)*current_test_count if total_pending > 0 and current_test_count > 0 else 0
        self.test_panel.update_result(progress_value, tid, s, st)

        self.test_panel.version_section.update()
        self.test_panel.project_section.update()
        self.test_panel.counter_section.update()
    
    def finalize_ui(self):
        self.test_panel.end_test()

        self.test_panel.version_section.update()

    def launch_test(self, coollab_path:str):
        if self.preview_panel:
            self.preview_panel.start_test()
            self.preview_panel.image_section.update()
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
                time.sleep(0.5)

                score = test_data["score"]
                status = True
                # self.page.run_thread(lambda tid=test_id, s=score, st=status: self.update_single_test_result(current_test_count, total_pending, tid, s, st))
                self.update_single_test_result(current_test_count, total_pending, test_id, score, status)

            self.finalize_ui()
