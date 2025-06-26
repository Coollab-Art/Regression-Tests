import subprocess
from pathlib import Path
from time import sleep
from services.Coollab import Coollab

def start_coollab(coollab_path: Path):
    if not coollab_path.exists():
        raise FileNotFoundError(f"coollab.exe not found at: {coollab_path}")

    try:
        process = subprocess.Popen([
            str(coollab_path)
            # '--open_project',
            # str(project_path)
        ])
    except Exception as e:
        raise RuntimeError(f"Failed to launch Coollab: {e}")
    

def test_coollab():
    with Coollab() as coollab:
        i = 0
        while i < 10:
            i += 1
            if i % 2 == 0:
                coollab.export_image(filename="Test", width=800, height=800, format="png", path="C:\\Users\\elvin\\Documents\\IMAC\\Coollab")
            else:
                coollab.log("Scripting", f"This is a script! {i}")
            sleep(1)