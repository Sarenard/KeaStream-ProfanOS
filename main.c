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

void add_buffer(char* code, InstPile *liste_instructions) {
    // Instpile_push(liste_instructions, (Instruction) {
    //     .name = "thing",
    //     .element = (Element) {
    //         .data_type = 1,
    //         .data_int = 0,
    //         .data_string = code
    //     }
    // });
    
}

void compileall(char* code, InstPile liste_instructions) {
    int index = 0;
    char *buffer = calloc(sizeof(char) * 100, sizeof(char));
    int nb_fleches = 0;
    while (index < strlen(code)) {
        if (code[index] == '>') {
            if (strlen(buffer) > 0) {
                char* buffer2 = calloc(sizeof(char) * 100, sizeof(char));
                strcpy(buffer2, buffer);
                add_buffer(buffer2, &liste_instructions);
                for (int i = 0; i < 100; i++) {
                    buffer[i] = '\0';
                }
            }
            nb_fleches++;
            index++;
            continue;
        }
        if (nb_fleches != 0) {
            Instpile_push(&liste_instructions, (Instruction) {
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
    for (int i = 0; i < liste_instructions.top; i++) {
        printf("inst[%d] : %s %d %d %s\n", i, liste_instructions.inst[i].name, liste_instructions.inst[i].element.data_type, liste_instructions.inst[i].element.data_int, liste_instructions.inst[i].element.data_string);
    }
}

int main() {
    printf("Lancement du programme c\n");
    char *code = "1,2,3,4>>>>+,+>>+>print";
    int code_size = strlen(code);
    InstPile liste_instructions = Instpile_init(code_size);
    compileall(code, liste_instructions);
    return 0;
}