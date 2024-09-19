import glob
import subprocess


for path in glob.glob("*.desktop"):
    filename = path.strip().split('/')[-1]
    subprocess.call(["chmod", "+x", path])
    subprocess.call(["ln", "-s", path, f"~/Desktop/{filename}"])
