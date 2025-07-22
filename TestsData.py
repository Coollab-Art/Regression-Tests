from dataclasses import dataclass
from slugify import slugify
from pathlib import Path

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

    def get_ref_file_path(self, folder: Path = Path("assets/img/ref")) -> Path | None:
        for file in folder.glob(f"{self.name}.*"):
            if file.is_file():
                # print("File found : "+str(file.resolve()))
                return file.resolve()
        return None
    
    def get_project_file_path(self) -> Path:
        return (Path("assets/projects") / f"{self.name}.coollab").resolve()

def get_test_data():
    # TODO parse folder
    return [
        TestData(1, project_name="BlackHole"),
        TestData(2, project_name="fractale"),
        TestData(3, project_name="bruit"),
        TestData(4, project_name="rond"),
    ]
