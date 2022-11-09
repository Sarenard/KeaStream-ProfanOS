import subprocess
import os

command = "mypy .\main.py"
print(f"| {command}")
try:
    result = subprocess.check_output(command.split(" "))
except:
    print("| mypy failed :")
    os.system(command)
    exit(1)
command = "python .\main.py"
print(f"| {command}")
os.system(command)
