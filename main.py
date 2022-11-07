from typing import List

class Element:
    def __init__(self, data_type: int, data_int: int, data_str: str):
        self.data_type: int = data_type
        self.data_int: int = data_int
        self.data_str: str = data_str
    def __repr__(self):
        if self.data_type == 0:
            return f"int({self.data_int})"
        elif self.data_type == 1:
            return f"str(\"{self.data_str}\")"
        
class Instruction:
    def __init__(self, name:str, args:List[Element]):
        self.name:str = name
        self.args:List[Element] = args
    def __repr__(self):
        return f"Instruction({self.name}, {self.args})"

class ElementPile:
    def __init__(self, size_max:int, elements: List[Element]):
        self.elements:List[Element] = []
        self.size_max:int = size_max
        self.size:int = 0
    def __repr__(self):
        return f"ElementPile({self.elements})"
        
class InstructionPile:
    def __init__(self, size_max:int, elements: List[Instruction]):
        self.elements:List[Instruction] = []
        self.size_max:int = size_max
        self.size:int = 0
    def __repr__(self):
        return f"InstructionPile({self.elements})"

def add_ElementPile(pile:ElementPile, element:Element) -> None:
    if pile.size == pile.size_max:
        print("Erreur, la pile esst trop grande")
        exit(1)
    pile.elements.append(element)
    pile.size += 1
    
def remove_ElementPile(pile) -> Element:
    pile.size -= 1
    return pile.elements.pop()

def add_InstructionPile(pile:InstructionPile, element:Instruction) -> None:
    if pile.size == pile.size_max:
        print("Erreur, la pile esst trop grande")
        exit(1)
    pile.elements.append(element)
    pile.size += 1
    
def remove_InstructionPile(pile) -> Instruction:
    pile.size -= 1
    return pile.elements.pop()

def instruction_from_data(data:str) -> Element:
    liste_nombres:List[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    is_number:int = 1
    for i in range(len(data)):
        in_list:int = 0
        for j in range(len(liste_nombres)):
            if data[i] == liste_nombres[j]:
                in_list = 1
                break
        if in_list == 0:
            is_number = 0
            break
    if is_number:
        return Instruction("push", Element(0, int(data), ""))
    is_string:int = 1
    if data[0] != "\"" or data[-1] != "\"":
        is_string = 0
    if is_string:
        return Instruction("push", Element(1, 0, data[1:-1]))
    return Instruction("cmd", Element(1, 0, data))

def compile(code : str, liste_instructions : InstructionPile) -> None:
    code += " "
    buffer : str = ""
    for i in range(len(code)):
        if code[i] == " ":
            if buffer == "":
                continue
            add_InstructionPile(liste_instructions, instruction_from_data(buffer))
            buffer = ""
        else:
            buffer += code[i]

def run(liste_instructions : InstructionPile) -> None:
    pass

def main():
    code:str = """1 2 + ."""
    liste_instructions:InstructionPile = InstructionPile(100, [])
    compile(code, liste_instructions)
    print(liste_instructions)
    run(liste_instructions)
    
main()