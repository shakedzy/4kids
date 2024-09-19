import os
import glob
import subprocess
from pathlib import Path


home = str(Path.home())
working_dir = os.getcwd()
_, dirs, _ = next(os.walk(working_dir))

for folder in dirs:
    print(folder)
    desktop_file = glob.glob(f"{folder}/*.desktop")[0]
    with open(desktop_file, 'r') as f:
        desktop_script = f.read()
    desktop_script = desktop_script.replace("%k", working_dir)
    with open(f"{home}/Desktop/{desktop_file.split('/')[-1]}", 'w') as f:
        f.write(desktop_script)
    python_file =  glob.glob(f"{folder}/*.py")[0]
    subprocess.call(["chmod", "+x", python_file])
