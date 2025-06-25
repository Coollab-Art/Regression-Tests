import subprocess
from pathlib import Path
from time import sleep
from services.Coollab import Coollab

class CoollabHandler:
    def __init__(self):
        self.process = None

    def start(self, coollab_path: str):
        coollab_path = Path(coollab_path)
        if not coollab_path.exists():
            raise FileNotFoundError(f"coollab.exe not found at: {coollab_path}")

        try:
            self.process = subprocess.Popen([
                str(coollab_path)
                # '--open_project',
                # str(self.project_path)
            ])
        except Exception as e:
            raise RuntimeError(f"Failed to launch Coollab: {e}")
    
    def launch_project(self, project_path: str):
        project_path = Path(project_path)
        if not project_path.exists():
            raise FileNotFoundError(f"Project file not found: {self.project_path}")
        
        # with Coollab() as coollab:
            # coollab.launch_project(project_path)

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            # self.process.wait()
        else:
            print("Coollab is not running or already terminated.")

    def export_coollab_img(self, name: str, width: int = None, height: int = None):
        export_folder_path = str(Path().resolve() / "assets" / "img" / "exp")
        with Coollab() as coollab:
            coollab.export_image(path=export_folder_path, filename=name, format="png", width=800, height=800)

    def close_coollab(self, force_kill: bool):
        with Coollab() as coollab:
            coollab.close_app(force_kill=force_kill)

    def open_project(self, path: str):
        with Coollab() as coollab:
            coollab.open_project(project_path=path)
        

    def test_coollab(self):
        with Coollab() as coollab:
            i = 0
            while i < 10:
                i += 1
                if i % 2 == 0:
                    coollab.export_image(filename="Test", width=800, height=800, format="png", path="C:\\Users\\elvin\\Documents\\IMAC\\Coollab")
                else:
                    coollab.log("Scripting", f"This is a script! {i}")
                sleep(1)