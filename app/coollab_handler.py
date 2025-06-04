import subprocess
from pathlib import Path
import time

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
    time.sleep(3)
    process.terminate()
    # try:
    #     process = subprocess.Popen(command)
    #     time.sleep(3)
    #     process.terminate()
    # except FileNotFoundError:
    #     print(f"Erreur: Coollab.exe n'a pas été trouvé à l'emplacement: {coollab_path}")
    # except PermissionError:
    #     print(f"Erreur: Accès refusé pour exécuter {coollab_path}")
    # except Exception as e:
    #     print(f"Une erreur inattendue est survenue lors du lancement de Coollab: {e}")