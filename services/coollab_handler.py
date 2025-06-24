import subprocess
from pathlib import Path
from time import sleep
from Coollab import Coollab

def open_coollab_project(coollab_path: str, project_path: str):

    coollab_path = Path(coollab_path)
    project_path = Path(project_path)
    command = [
        coollab_path,
        '--open_project',
        project_path
    ]

    if not coollab_path.exists():
        raise FileNotFoundError(f"coollab.exe not found at: {coollab_path}")
    if not project_path.exists():
        raise FileNotFoundError(f"Project file not found: {project_path}")
    process = subprocess.Popen(command)
    sleep(3)
    
    process.terminate()
    # try:
    #     process = subprocess.Popen(command)
    #     sleep(3)
    #     process.terminate()
    # except FileNotFoundError:
    #     print(f"Erreur: Coollab.exe n'a pas été trouvé à l'emplacement: {coollab_path}")
    # except PermissionError:
    #     print(f"Erreur: Accès refusé pour exécuter {coollab_path}")
    # except Exception as e:
    #     print(f"Une erreur inattendue est survenue lors du lancement de Coollab: {e}")

def test_coollab():
    with Coollab() as coollab:
        i = 0
        while i < 10:
            i += 1
            if i % 2 == 0:
                coollab.export_image(width=500, height=500)
            else:
                coollab.log("Scripting", f"This is a script! {i}")
            sleep(1)