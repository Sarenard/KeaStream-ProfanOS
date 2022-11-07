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
    char* data_string;
} Element;

typedef struct Instruction {
    char *name;
    Element element;
} Instruction;

typedef struct InstPile {
    Instruction *inst;
    int size;
    int top;
} InstPile;

InstPile Instpile_init(int size) {
    InstPile pile;
    pile.inst = malloc(sizeof(Instruction) * size);
    pile.size = size;
    pile.top = -1;
    return pile;
}

void Instpile_push(InstPile *pile, Instruction inst) {
    if (pile->top == pile->size - 1) {
        printf("Stack overflow");
    }
    pile->inst[++pile->top] = inst;
}

Instruction Instpile_pop(InstPile *pile) {
    if (pile->top == -1) {
        printf("Stack underflow");
    }
    return pile->inst[pile->top--];
}

typedef struct Pile {
    Element* elements;
    int size;
    int top;
} Pile;

Pile pile_init(int size) {
    Pile pile;
    pile.elements = malloc(sizeof(Element) * size);
    pile.size = size;
    pile.top = -1;
    return pile;
}

void pile_push(Pile *pile, Element element) {
    if (pile->top == pile->size - 1) {
        printf("Stack overflow");
    }
    pile->elements[++pile->top] = element;
}

Element pile_pop(Pile *pile) {
    if (pile->top == -1) {
        printf("Stack underflow");
    }
    return pile->elements[pile->top--];
}

typedef struct Function {
    int nb_args;
    int nb_return;
    int function;
} Function;

void add2int(Pile *pile, Pile *liste_args) {
    Element arg1 = pile_pop(liste_args);
    Element arg2 = pile_pop(liste_args);
    if (arg1.data_type == 0 && arg2.data_type == 0) {
        Element res;
        res.data_type = 0;
        res.data_int = arg1.data_int + arg2.data_int;
        pile_push(pile, res);
        return;
    }
}

void afficher(Pile *pile, Pile *liste_args) {
    Element arg1 = pile_pop(liste_args);
    if (arg1.data_type == 0) {
        printf("%d", arg1.data_int);
        return;
    }
}

#define NB_BUILDINS 2
#define NB_ALIAS_MAX 3

char *buildins_names[NB_BUILDINS][NB_ALIAS_MAX] = {
    {"add", "+", ""},
    {"print", "afficher", ""}
};

Function buildins_functions[NB_BUILDINS] = {
    (Function){2, 1, (int)add2int},
    (Function){1, 0, (int)afficher}
};

void add_instruction(char* inst, InstPile *liste_instructions) {
    int is_num = 1;
    char* liste_num = "0123456789";
    for (int i = 0; i < strlen(inst); i++) {
        int temp = 0;
        for (int j=0; j<strlen(liste_num); j++) {
            if (inst[i] == liste_num[j]) {
                temp = 1;
            }
        }
        if (temp == 0) {
            is_num = 0;
        }
    }
    if (is_num == 1) {
        int nb = 0;
        nb = ascii_to_int(inst);
        Instpile_push(liste_instructions, (Instruction) {
            .name = "addnb",
            .element = (Element) {
                .data_type = 0,
                .data_int = nb,
                .data_string = ""
            }
        });
    } else {
        Instpile_push(liste_instructions, (Instruction) {
            .name = "cmd",
            .element = (Element) {
                .data_type = 1,
                .data_int = 0,
                .data_string = inst
            }
        });
    }
}

void add_buffer(char* buffer1, InstPile *liste_instructions) {
    int index = 0;
    char* buffer2 = malloc(sizeof(char) * 100);
    for (int i=0; i<100; i++) {
        buffer2[i] = '\0';
    }
    while (index < strlen(buffer1)) {
        if (buffer1[index] == ',') {
            if (strlen(buffer2) != 0) {
                char* buffer3 = malloc(sizeof(char) * 100);
                strcpy(buffer3, buffer2);
                add_instruction(buffer3, liste_instructions);
                for (int i = 0; i < strlen(buffer2); i++) {
                    buffer2[i] = '\0';
                }
            } 
        } else {
            buffer2[strlen(buffer2)] = buffer1[index];
            buffer2[strlen(buffer2)] = '\0';
        }
        index++;
    }
    char* buffer3 = malloc(sizeof(char) * 100);
    strcpy(buffer3, buffer2);
    add_instruction(buffer3, liste_instructions);
}

void compileall(char* code, InstPile *liste_instructions) {
    int index = 0;
    char *buffer = malloc(sizeof(char) * 100);
    for (int i=0; i<100; i++) {
        buffer[i] = '\0';
    }
    int nb_fleches = 0;
    while (index < strlen(code)) {
        if (code[index] == '>') {
            if (strlen(buffer) > 0) {
                char* buffer2 = malloc(sizeof(char) * 100);
                for (int i=0; i<100; i++) {
                    buffer2[i] = '\0';
                }
                strcpy(buffer2, buffer);
                add_buffer(buffer2, liste_instructions);
                for (int i = 0; i < 100; i++) {
                    buffer[i] = '\0';
                }
            }
            nb_fleches++;
            index++;
            continue;
        }
        if (nb_fleches != 0) {
            Instpile_push(liste_instructions, (Instruction) {
                .name = "fleche",
                .element = (Element) {
                    .data_type = 0,
                    .data_int = nb_fleches,
                    .data_string = ""
                }
            });
            nb_fleches = 0;
        }
        buffer[strlen(buffer)] = code[index];
        buffer[strlen(buffer) + 1] = '\0';
        index++;
    }
    char* buffer2 = malloc(sizeof(char) * 100);
    for (int i=0; i<100; i++) {
        buffer2[i] = '\0';
    }
    strcpy(buffer2, buffer);
    add_buffer(buffer2, liste_instructions);
}

void run(InstPile *liste_instructions) {
    Pile pile = pile_init(100);
    Pile work_pile = pile_init(100);
    for (int i = 0; i < liste_instructions->top+1; i++) {
        // if (liste_instructions->inst[i].element.data_type == 0) {
        //     printf("inst[%d] = Instruction(%s, Element(%d))\n", i, liste_instructions->inst[i].name, liste_instructions->inst[i].element.data_int);
        // } else {
        //     printf("inst[%d] = Instruction(%s, Element(\"%s\"))\n", i, liste_instructions->inst[i].name, liste_instructions->inst[i].element.data_string);
        // }
        Instruction inst = liste_instructions->inst[i];
        if (!strcmp(inst.name, "addnb")) {
            // printf("addnb\n");
            pile_push(&pile, inst.element);
        } else if (!strcmp(inst.name, "fleche")) {
            // printf("fleche\n");
            for (int j=0; j<work_pile.top+1; j++) {
                pile_push(&pile, work_pile.elements[j]);
            }
            for (int j=0; j<inst.element.data_int; j++) {
                pile_push(&work_pile, pile_pop(&pile));
            }
        } else if (!strcmp(inst.name, "cmd")) {
            // printf("cmd\n");
            for (int liste_id = 0; liste_id < NB_BUILDINS; liste_id++) {
                for (int alias_id = 0; alias_id < NB_ALIAS_MAX; alias_id++) {
                    if (!strcmp(buildins_names[liste_id][alias_id], inst.element.data_string)) {
                        Function func = buildins_functions[liste_id];
                        // printf("func = %s\n", buildins_names[liste_id][alias_id]);
                        ((void (*)(Pile*, Pile*)) func.function)(&pile, &work_pile);
                    }
                }
            }
        }
        free(inst.element.data_string);
    }
    free(pile.elements);
    free(work_pile.elements);
}


int main() {
    char *code = "1,2,3,4>>>>+,+>>+>print";
    int code_size = strlen(code);
    InstPile liste_instructions = Instpile_init(code_size);
    compileall(code, &liste_instructions);
    run(&liste_instructions);
    for (int i = 0; i < liste_instructions.top+1; i++) {
        free(liste_instructions.inst[i].element.data_string);
    }
    free(liste_instructions.inst);
    return 0;
}