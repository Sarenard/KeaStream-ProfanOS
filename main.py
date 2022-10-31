from typing import List

class Function:
    def __init__(self, nb_args: int, nb_return: int, function: int):
        self.nb_args:int = nb_args
        self.nb_return:int = nb_return
        self.function:int = function

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

class Pile:
    def __init__(self, size_max:int, elements: List[Element]):
        self.elements:List[Element] = []
        self.size_max:int = size_max
        self.size:int = 0

def add_pile(pile:Pile, element:Element) -> None:
    if pile.size == pile.size_max:
        print("Erreur, la pile esst trop grande")
        exit(1)
    pile.elements.append(element)
    pile.size += 1
    
def remove_pile(pile) -> Element:
    pile.size -= 1
    return pile.elements.pop()

class Instruction:
    def __init__(self, name:str, args:List[Element]):
        self.name:str = name
        self.args:List[Element] = args
    def __repr__(self):
        return f"Instruction({self.name}, {self.args})"
    
def add2int(pile:Pile, liste_args:Pile) -> None:
    x = remove_pile(liste_args)
    y = remove_pile(liste_args)
    if x.data_type == 0 and y.data_type == 0:
        add_pile(pile, Element(0, x.data_int + y.data_int, ""))

def afficher(pile:Pile, liste_args:Pile) -> None:
    x = remove_pile(liste_args)
    if x.data_type == 0:
        print(x.data_int)

buildins_names = [["add", "+"], ["print"]]
buildins_funcs = [Function(2, 1, add2int), Function(1, 0, afficher)]

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
    nb_fleches = 0
    while index < len(code):
        if code[index] == ">":
            if len(buffer) != 0:
                add_buffer(buffer, liste_instructions)
                buffer = ""
            nb_fleches += 1
            index += 1
            continue
        if nb_fleches != 0:
            liste_instructions.append(Instruction("fleche", [Element(0, nb_fleches, "")]))
            nb_fleches = 0
        buffer += code[index]
        index += 1
    add_buffer(buffer, liste_instructions)

def run(liste_instructions:List[Instruction]) -> None:
    stack = Pile(100, [])
    work_pile = Pile(100, [])
    for i in range(len(liste_instructions)):
        inst:Instruction = liste_instructions[i]
        print(f"{inst.name + ' '*(10-len(inst.name))} : {inst}")
        if inst.name == "addnb":
            add_pile(stack, inst.args[0])
        elif inst.name == "cmd":
            for liste_id in range(len(buildins_names)):
                for element_id in range(len(buildins_names[liste_id])):
                    if inst.args[0].data_str == buildins_names[liste_id][element_id]:
                        if work_pile.size >= buildins_funcs[liste_id].nb_args:
                            buildins_funcs[liste_id].function(stack, work_pile)
                        else:
                            print(f"Erreur, pas assez d'arguments pour la fonction {inst.args[0].data_str}, espected {buildins_funcs[liste_id].nb_args}, reçu {work_pile.size}")
                            exit(1)
        elif inst.name == "fleche":
            for i in range(work_pile.size):
                add_pile(stack, remove_pile(work_pile))
            for i in range(inst.args[0].data_int):
                add_pile(work_pile, remove_pile(stack))
        print(f"stack     : {stack.elements}")
        print(f"work_pile : {work_pile.elements}")
        print()

if __name__ == "__main__":
    code = """1,2,3,4>>>>+,+>>+>print"""
    liste_instructions = []
    compileall(code, liste_instructions)
    run(liste_instructions)