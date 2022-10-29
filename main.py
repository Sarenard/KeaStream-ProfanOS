from dataclasses import dataclass
from typing import List

liste_buildins = ["+", "add"]

@dataclass
class Element:
    data_type: int
    data_int: int
    data_str: str

@dataclass
class Pile:
    size_max: int
    elements: List[Element]
    size: int = 0

def add_pile(pile:Pile, element:Element) -> None:
    if pile.size == pile.size_max:
        print("Erreur, la pile esst trop grande")
        exit(1)
    pile.elements.append(element)
    pile.size += 1
    
def remove_pile(pile) -> Element:
    pile.size -= 1
    return pile.elements.pop()

@dataclass
class Instruction:
    name: str
    args: List[Element]

def add_instruction(inst:str, liste_instructions:List[Instruction]) -> None:
    is_num = True
    liste_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(len(inst)):
        temp = False
        for j in range(len(liste_num)):
            if inst[i] == liste_num[j]:
                temp = True
        if not temp:
            is_num = False
    if is_num:
        liste_instructions.append(Instruction("addnb", [Element(0, int(inst), "")]))
    else:
        liste_instructions.append(Instruction("cmd", [Element(1, 0, inst)]))

def add_buffer(buffer1:str, liste_instructions:List[Instruction]) -> None:
    index = 0
    buffer2 = ""
    while index < len(buffer1):
        if buffer1[index] == ",":
            if len(buffer2) != 0:
                add_instruction(buffer2, liste_instructions)
                buffer2 = ""
        else:
            buffer2 += buffer1[index]
        index += 1
    add_instruction(buffer2, liste_instructions)

def compileall(code:str, liste_instructions:List[Instruction]) -> None:
    if code[len(code)-1] == ">":
        print("Erreur, on ne peut pas finir par >")
        exit(1)
    index = 0
    buffer = ""
    while index < len(code):
        if code[index] == ">":
            if len(buffer) != 0:
                add_buffer(buffer, liste_instructions)
                buffer = ""
        else:
            buffer += code[index]
        index += 1
    add_buffer(buffer, liste_instructions)

def run(liste_instructions:List[Instruction]) -> None:
    stack = Pile(100, [])
    for i in range(len(liste_instructions)):
        inst:Instruction = liste_instructions[i]
        if inst.name == "addnb":
            add_pile(stack, inst.args[0])
        elif inst.name == "cmd":
            print(f"command : {inst}")

if __name__ == "__main__":
    code = """1,2>>+>print"""
    liste_instructions = []
    compileall(code, liste_instructions)
    run(liste_instructions)