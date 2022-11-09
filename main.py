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
    def __init__(self, name:str, data_type:int, data_Element, data_Instruction):
        self.name:str = name
        self.data_type:int = data_type
        self.data_Element:ElementPile = data_Element
        self.data_Instruction:InstructionPile = data_Instruction
    def __repr__(self):
        return f"Instruction(\"{self.name}\", {self.data_type}, {self.data_Element}, {self.data_Instruction})"

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

def instruction_from_data(data:str) -> Instruction:
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
    liste_elements:ElementPile = ElementPile(100, [])
    liste_instructions:InstructionPile = InstructionPile(100, [])
    
    if is_number:
        add_ElementPile(liste_elements, Element(0, int(data), ""))
        return Instruction("push", 0, liste_elements, liste_instructions)
    is_string:int = 1
    if data[0] != "\"" or data[-1] != "\"":
        is_string = 0
    if is_string:
        add_ElementPile(liste_elements, Element(1, 0, data[1:-1]))
        return Instruction("push", 0, liste_elements, liste_instructions)

    add_ElementPile(liste_elements, Element(1, 0, data))
    return Instruction("cmd", 0, liste_elements, liste_instructions)

def compile(code : str, liste_instructions : InstructionPile) -> None:
    code += " "
    buffer : str = ""
    i:int = 0
    while i < len(code):
        if code[i] == " ":
            if buffer == "":
                pass
            elif buffer == "if":
                bufferIf:str = ""
                to_compile:str = ""
                i += 1
                end_count:int = 0
                start_count:int = 1
                while i < len(code):
                    to_compile += code[i]
                    if code[i] == " ":
                        if bufferIf == "":
                            pass
                        elif bufferIf == "if":
                            start_count += 1
                        elif bufferIf == "end":
                            end_count += 1
                            if end_count == start_count:
                                break
                        bufferIf = ""
                    else:
                        bufferIf += code[i]
                    i += 1
                    instructionPileIf = InstructionPile(100, [])
                compile(to_compile, instructionPileIf)
                elementsIf = ElementPile(100, [])
                add_ElementPile(elementsIf, Element(1, 0, "if"))
                add_InstructionPile(liste_instructions, Instruction("cmd", 1, elementsIf, instructionPileIf))
                buffer = ""
            else:
                if buffer == "end":
                    pass
                else:
                    add_InstructionPile(liste_instructions, instruction_from_data(buffer))
                    buffer = ""
        else:
            buffer += code[i]
        i += 1
    # reverse liste_instructions
    for i in range(liste_instructions.size // 2):
        tmp:Instruction = liste_instructions.elements[i]
        liste_instructions.elements[i] = liste_instructions.elements[liste_instructions.size - i - 1]
        liste_instructions.elements[liste_instructions.size - i - 1] = tmp

def run(stack:ElementPile, liste_instructions : InstructionPile) -> None:
    for i in range(liste_instructions.size):
        instruction:Instruction = remove_InstructionPile(liste_instructions)
        instruction_elements:ElementPile = instruction.data_Element
        # command_element:Element = remove_ElementPile(instruction_elements)
        if instruction.name == "push":
            elementPush:Element = remove_ElementPile(instruction_elements)
            add_ElementPile(stack, elementPush)
        elif instruction.name == "cmd":
            command_name:Element = remove_ElementPile(instruction_elements)
            # TODO : recode this with external functions
            if command_name.data_str == ".":
                elementPrint1:Element = remove_ElementPile(stack)
                print(elementPrint1)
            elif command_name.data_str == "+":
                elementAdd1:Element = remove_ElementPile(stack)
                elementAdd2:Element = remove_ElementPile(stack)
                add_ElementPile(stack, Element(0, elementAdd1.data_int + elementAdd2.data_int, ""))
            elif command_name.data_str == "dup":
                elementDup1:Element = remove_ElementPile(stack)
                add_ElementPile(stack, elementDup1)
                add_ElementPile(stack, elementDup1)
            elif command_name.data_str == "if":
                elementIf1:Element = remove_ElementPile(stack)
                if elementIf1.data_type == 0:
                    if elementIf1.data_int != 0:
                        run(stack, instruction.data_Instruction)
                elif elementIf1.data_type == 1:
                    if len(elementIf1.data_str) > 0:
                        run(stack, instruction.data_Instruction)
            else:
                print(f"Commande inconnue : {command_name.data_str}")
                exit(1)

def main() -> None:
    code:str = """3 dup if 4 + end . 0 dup if 4 + end ."""
    print(f"lancement du code : \"{code}\"")
    liste_instructions:InstructionPile = InstructionPile(100, [])
    compile(code, liste_instructions)
    stack:ElementPile = ElementPile(100, []) 
    run(stack, liste_instructions)
    
main()