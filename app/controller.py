class Controller:
    def __init__(self, page):
        self.page = page
        self.preview_panel = None

    def set_preview_panel(self, panel):
        self.preview_panel = panel

    def set_test_panel(self, panel):
        self.test_panel = panel

    def update_preview(self, test_id: str):
        result = f"Image test {test_id}"
        print(f"[Controller] Switch image: Test {test_id} → {result}")

        if self.preview_panel:
            self.preview_panel.update_content(result)
