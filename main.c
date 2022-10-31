#include <stdlib.h>
#include <string.h>
#include <stdio.h>

//DO NOT PORT THIS
int ascii_to_int(char str[]) {
    int i, n;
    n = 0;
    for (i = 0; str[i] != '\0'; ++i)
        n = n * 10 + str[i] - '0';
    return n;
}

typedef struct Element {
    int data_type;
    int data_int;
    char *data_str;
} Element;

typedef struct Instruction {
    char *name;
    Element element;
} Instruction;

typedef struct Function {
    int nb_args;
    int nb_return;
    int function;
} Function;

typedef struct Pile {
    Element* elements;
    int size_max;
    int size;
} Pile;

typedef struct PileInst {
    Instruction* elements;
    int size_max;
    int size;
} PileInst;

Pile pile_init(int size_max) {
    Pile pile;
    pile.size_max = size_max;
    pile.size = 0;
    pile.elements = malloc(size_max*sizeof(Element));
    return pile;
}

void free_pile(Pile pile) {
    free(pile.elements);
}

void add_pile(Pile pile, Element element) {
    if (pile.size == pile.size_max) {
        printf("Erreur, la pile est trop grande");
        return;
    }
    pile.elements[pile.size] = element;
    pile.size += 1;
}

Element remove_pile(Pile pile) {
    Element element = pile.elements[pile.size];
    pile.size -= 1;
    return element;
}

PileInst pileinst_init(int size_max) {
    PileInst pile;
    pile.size_max = size_max;
    pile.size = 0;
    pile.elements = malloc(size_max*sizeof(Instruction));
    return pile;
}

void free_pileinst(PileInst pile) {
    free(pile.elements);
}

void add_pileinst(PileInst pile, Instruction element) {
    if (pile.size == pile.size_max) {
        printf("Erreur, la pile est trop petite");
        return;
    }
    pile.elements[pile.size] = element;
    pile.size += 1;
}

Instruction remove_pileinst(PileInst pile) {
    Instruction element = pile.elements[pile.size];
    pile.size -= 1;
    return element;
}

void add2(Pile pile, Pile liste_args) {
    Element x = remove_pile(liste_args);
    Element y = remove_pile(liste_args);
    if (x.data_type == 0 && y.data_type == 0) {
        Element current;
        current.data_type = 0;
        current.data_int = x.data_int + y.data_int;
        current.data_str = malloc(0);
        return; 
    }
}

void afficher(Pile pile, Pile liste_args) {
    Element x = remove_pile(liste_args);
    if (x.data_type == 0) {
        printf("%d", x.data_int);
    }
}


#define NB_BUILDINS 2
#define MAX_ALIAS 3
char *buildins_names[NB_BUILDINS][MAX_ALIAS] = {
    {"add", "+", ""},
    {"print", "", ""}
};
Function buildins_funcs[NB_BUILDINS] = {
    (Function){2, 1, (int) add2},
    (Function){1, 0, (int) afficher}
};

void add_instruction(char *inst, PileInst liste_instructions) {
    int is_num = 1;
    int temp;
    char liste_num[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
    for (int i = 0; i < strlen(inst); i++) {
        temp = 0;
        for (int j = 0; j < 10; j++) {
            if (inst[i] == liste_num[j]) {
                temp = 1;
            }
            if (temp == 0) {
                is_num = 0;
            }
        }
    }
    if (is_num) {
        add_pileinst(liste_instructions, (Instruction){"addnb", (Element){0, ascii_to_int(inst), ""}});
    } else {
        add_pileinst(liste_instructions, (Instruction){"cmd", (Element){1, 0, inst}});
    }
}

void add_buffer(char *buffer1, PileInst liste_instructions) {
    int index = 0;
    char buffer2[100];
    while (index < strlen(buffer1)) {
        if (buffer1[index] == ',') {
            if (strlen(buffer2) != 0) {
                add_instruction(buffer2, liste_instructions);
                buffer2[0] = '\0';
            }
        } else {
            buffer2[strlen(buffer2)] = buffer1[index];
            buffer2[strlen(buffer2)+1] = '\0';
        }
        index += 1;
    }
    if (strlen(buffer2) != 0) {
        add_instruction(buffer2, liste_instructions);
    }
}

void compileall(char* code, PileInst liste_instructions) {
    if (code[strlen(code) - 1] == '>') {
        printf("Erreur, le code ne doit pas finir par >");
        return;
    }
    int index = 0;
    char buffer[100];
    int nb_fleches = 0;
    while (index < strlen(code)) {
        if (code[index] == '>') {
            if (strlen(buffer) != 0) {
                add_buffer(buffer, liste_instructions);
                buffer[0] = '\0';
            }
            nb_fleches++;
            index++;
            continue;
        }
        if (nb_fleches != 0) {
            printf("%d\n", liste_instructions.size);
            add_pileinst(liste_instructions, (Instruction){"fleche", (Element){0, nb_fleches, ""}});
            printf("%d\n", liste_instructions.size);
            nb_fleches = 0;
        }
        buffer[strlen(buffer)] = code[index];
        buffer[strlen(buffer)+1] = '\0';
        index += 1;
    }
    if (strlen(buffer) != 0) {
        add_buffer(buffer, liste_instructions);
    }
}

void run(PileInst liste_instructions) {
    Pile stack = pile_init(100);
    Pile work_pile = pile_init(100);
    for (int i = 0; i < liste_instructions.size; i++) {
        Instruction inst = remove_pileinst(liste_instructions);
        printf("INST : %s", inst.name);
        if (strcmp("addnb", inst.name)) {
            add_pile(stack, inst.element);
        }
        else if (strcmp("fleche", inst.name)) {
            for (int i=0; i < work_pile.size; i++) {
                add_pile(stack, remove_pile(work_pile));
            }
            for (int i=0; i < inst.element.data_int; i++) {
                add_pile(work_pile, remove_pile(stack));
            }
        }
        else if (strcmp("cmd", inst.name)) {
            for (int liste_id; liste_id < NB_BUILDINS; liste_id++) {
                for (int element_id; element_id < MAX_ALIAS; element_id++) {
                    if (strcmp(buildins_names[liste_id][element_id], inst.element.data_str)) {
                        if (work_pile.size >= buildins_funcs[liste_id].nb_args) {
                            if (buildins_funcs[liste_id].nb_args == 0) {
                                printf("Fonction %s", buildins_names[liste_id][element_id]);
                            }
                            else if (buildins_funcs[liste_id].nb_args == 1) {
                                printf("Fonction %s avec %d", buildins_names[liste_id][element_id], remove_pile(work_pile).data_int);
                            }
                            else if (buildins_funcs[liste_id].nb_args == 2) {
                                printf("Fonction %s avec %d et %d", buildins_names[liste_id][element_id], remove_pile(work_pile).data_int, remove_pile(work_pile).data_int);
                            }
                        } else {
                            printf("Erreur, pas assez d'arguments");
                            return;
                        }
                    }
                }
            }
        }
    }
}

int main() {
    printf("Lancement du programme c\n");
    char *code = "1,2,3,4>>>>+,+>>+>print";
    PileInst liste_instructions = pileinst_init(100);
    compileall(code, liste_instructions);
    run(liste_instructions);
    return 0;
}