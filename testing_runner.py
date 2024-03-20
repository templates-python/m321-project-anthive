import subprocess
import threading
from time import sleep


def main():
    discovery_port = '61000'
    discovery_thread = threading.Thread(
        target=run_script,
        args=('./discovery/discovery_service.py', discovery_port)
    )
    discovery_thread.start()

    hive01_thread = threading.Thread(
        target=run_script,
        args=('./hives/hive2.py', discovery_port, '62001')
    )
    sleep(1)
    hive01_thread.start()

    game_thread = threading.Thread(
        target=run_script,
        args=('./game/game_service.py', discovery_port, '61001')
    )
    sleep(1)
    game_thread.start()

    discovery_thread.join(timeout=60)
    hive01_thread.join(timeout=60)
    game_thread.join(timeout=60)

    print("All scripts have finished executing.")


def run_script(script_name, discovery_port, service_port=''):
    interpreter = './venv/Scripts/python.exe'
    subprocess.run([interpreter, script_name, discovery_port, service_port])


if __name__ == '__main__':
    main()
