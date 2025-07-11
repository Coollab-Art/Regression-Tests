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