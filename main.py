from typing import List
from dataclasses import dataclass

liste_buildins = ["+", "add"]

@dataclass
class Instruction:
    name: str
    args: List[str] | None  

def compileall(code:str, liste_instruction) -> None:
    c_data = ""
    index = 0
    while True:
        if index >= len(code):
            print("Wut, on devrait pas arriver ici")
            break
        if 

if __name__ == "__main__":
    code = """1,2>>+>print"""
    liste_instructions = []
    compileall(code, liste_instructions)
    print(liste_instructions)