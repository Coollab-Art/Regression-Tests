from dataclasses import dataclass
from slugify import slugify

class TestStatus:
    PASSED: str = "Passed"
    FAILED: str = "Failed"
    READY: str = "Ready"
    IN_PROGRESS: str = "Loading"
    CHECKING: str = "Checking"

@dataclass
class TestData:
    id: int
    project_name: str
    name: str = ""
    score: float = 0.0
    status: TestStatus = TestStatus.CHECKING
    exported_img_path: str = ""
    results: dict = None

    def __post_init__(self):
        self.name = slugify(self.project_name)
        if self.results is None:
            self.results = {}
    def reset(self):
        self.score = 0.0
        self.status = TestStatus.READY
        self.results = {}

    def get_ref_file_path(self):
        return f"assets/img/ref/{self.name}.png"
    def get_project_file_path(self):
        return f"assets/projects/{self.name}.coollab"

def get_test_data():
    return [
        TestData(1, project_name="Black Hole"),
        TestData(2, project_name="fractale"),
        TestData(3, project_name="bruit"),
        TestData(4, project_name="rond"),
    ]
