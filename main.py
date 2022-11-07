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
        
class InstructionPile:
    def __init__(self, size_max:int, elements: List[Instruction]):
        self.elements:List[Instruction] = []
        self.size_max:int = size_max
        self.size:int = 0

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

def compile(code : str, liste_instructions : InstructionPile) -> None:
    pass

def run(liste_instructions : InstructionPile) -> None:
    pass

def main():
    code:str = "1 2 + ."
    liste_instructions:InstructionPile = InstructionPile(100, [])
    compile(code, liste_instructions)
    run(liste_instructions)
    
main()