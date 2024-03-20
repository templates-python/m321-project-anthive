import threading
import subprocess
from time import sleep
import os


def main():
    discovery_thread = threading.Thread(
        target=run_script, args=('', './discovery/discovery_service.py',)
    )
    discovery_thread.start()
    print("============== discovery started ================")

    hive01_thread = threading.Thread(
        target=run_script, args=('', './hives/hive1.py',)
    )
    print("============== hive started ================")
    sleep(1)
    hive01_thread.start()

    game_thread = threading.Thread(
        target=run_script, args=('', './game/game_service.py',)
    )
    sleep(1)
    game_thread.start()


    discovery_thread.join(timeout=60)
    hive01_thread.join(timeout=60)
    game_thread.join(timeout=60)

    print("All scripts have finished executing.")

def run_script(script_path, script_name):
    interpreter = './.venv/Scripts/python.exe'
    project_root = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
    script = os.path.join(script_path, script_name)
    
    # Ensure that the environment has the project root in the PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')
    
    # Run the script using the full path and the modified environment
    subprocess.run([interpreter, script], env=env)

if __name__ == '__main__':
    main()