import os

def print_and_run(command):
    print(f"| {command}")
    os.system(command)

print_and_run("gcc main.c -o main.exe")
print_and_run("main.exe")