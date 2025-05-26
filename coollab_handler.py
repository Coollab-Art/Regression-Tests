import subprocess
from pathlib import Path

def open_coollab_project(coollab_exe_path: str, project_path: str):

    coollab_exe = Path(coollab_exe_path)
    project = Path(project_path)

    if not coollab_exe.exists():
        raise FileNotFoundError(f"coollab.exe not found at: {coollab_exe}")
    if not project.exists():
        raise FileNotFoundError(f"Project file not found: {project}")
    # --open_project "my/file/name.coollab"

    subprocess.Popen([str(coollab_exe), str(project)])