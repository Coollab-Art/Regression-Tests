from dataclasses import dataclass
from slugify import slugify

@dataclass
class TestData:
    id: int
    name: str
    test_name: str = ""
    img_export_extension: str = ".png"
    score: float = 0.0
    status: bool = False
    results: dict = None

    def __post_init__(self):
        if self.results is None:
            self.results = {}
    def reset(self):
        self.score = 0.0
        self.status = False
        self.results = {}

    def get_name(self):
        return slugify(self.name)
    def get_ref_file_path(self):
        return f"assets/img/ref/{self.get_name()}.png"
    def get_exp_file_path(self):
        return f"assets/img/exp/{self.get_name()}{self.img_export_extension}"
    def get_project_file_path(self):
        return f"assets/projects/{self.get_name()}.coollab"

def get_test_data():
    return [
        TestData(1, name="Black Hole", test_name="BlackHole"),
        TestData(2, name="fractale", test_name="Fractale"),
        TestData(3, name="bruit", test_name="Bruit", img_export_extension=".jpg"),
        TestData(4, name="rond", test_name="Rond"),
    ]
