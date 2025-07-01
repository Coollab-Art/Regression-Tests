from dataclasses import dataclass

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

def get_test_data():
    return [
        TestData(1, name="Black Hole", test_name="BlackHole"),
        TestData(2, name="fractale", test_name="Fractale"),
        TestData(3, name="bruit", test_name="Bruit", img_export_extension=".jpg"),
        TestData(4, name="rond", test_name="Rond"),
    ]
