/* LC-2K Instruction-level simulator */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define NUMMEMORY 65536 /* maximum number of words in memory */
#define NUMREGS 8 /* number of machine registers */
#define MAXLINELENGTH 1000 
typedef struct stateStruct {
    int pc;
    int mem[NUMMEMORY];
    int reg[NUMREGS];
    int numMemory;
} stateType;

void printState(stateType *);
int convertNum(int num);

#define ADD 0
#define NOR 1
#define LW  2
#define SW  3
#define BEQ 4
#define JALR    5
#define HALT    6
#define NOOP    7

int main(int argc, char *argv[])
{
    char line[MAXLINELENGTH];
    stateType state;
    FILE *filePtr;

    if (argc != 2) {
        printf("error: usage: %s <machine-code file>\n", argv[0]);
        exit(1);
    }

    filePtr = fopen(argv[1], "r");
    if (filePtr == NULL) {
        printf("error: can't open file %s", argv[1]);
        perror("fopen");
        exit(1);
    }

    /* read in the entire machine-code file into memory */
    for (state.numMemory = 0; fgets(line, MAXLINELENGTH, filePtr) != NULL;
            state.numMemory++) {

        if (sscanf(line, "%d", state.mem+state.numMemory) != 1) {
            printf("error in reading address %d\n", state.numMemory);
            exit(1);
        }
        printf("memory[%d]=%d\n", state.numMemory, state.mem[state.numMemory]);
    }
		/* TODO: */
    state.pc = 0;
    memset(state.reg, 0, (sizeof(int) * NUMREGS));

    int cnt = 0;
    int is_halt = 0;
    while (state.pc > MAXLINELENGTH || *(state.mem) > NUMMEMORY){
        int instr = state.mem[state.pc];
        int opcode = instr >> 22;

        printState(&state);

        int regA = (instr >> 19) & 0b111;
        int regB = (instr >> 16) & 0b111;
        int destreg = instr & 0b111;
        int offset = instr & 0b1111111111111111;

        switch (opcode){
            case ADD:
                state.reg[destreg] = state.reg[regA] + state.reg[regB];
                break;
            case NOR:
                state.reg[destreg] = ~(state.reg[regA] | state.reg[regB]);
                break;
            case LW:
                state.reg[regB] = state.mem[convertNum(offset + state.reg[regA])];
                break;
            case SW:
                state.mem[convertNum(offset + state.reg[regA])] = state.reg[regB];
                break;
            case BEQ:
                if (state.reg[regA] == state.reg[regB])
                    state.pc += convertNum(offset);
                break;
            case JALR:
                state.reg[regB] = state.pc += 1;
                state.pc = state.reg[regA] - 1;
                break;
            case HALT:
                state.pc++, cnt++;
                is_halt = 1;
                break;
            case NOOP:
                break;
            default:
                printf("unknown opcode\n");
                break;
        }
        if (is_halt)
            break;

        state.pc++, cnt++;
    }

    printf("\nmachine halted\n");
    printf("total of %d instructions executed\n", cnt);
    printf("final state of macine:\n");

    printState(&state);

    fclose(filePtr);
    return(0);
}

void printState(stateType *statePtr)
{
    int i;
    printf("\n@@@\nstate:\n");
    printf("\tpc %d\n", statePtr->pc);
    printf("\tmemory:\n");
    for (i = 0; i < statePtr->numMemory; i++) {
        printf("\t\tmem[ %d ] %d\n", i, statePtr->mem[i]);
    }
    printf("\tregisters:\n");
    for (i = 0; i < NUMREGS; i++) {
        printf("\t\treg[ %d ] %d\n", i, statePtr->reg[i]);
    }
    printf("end state\n");
}

int convertNum(int num)
{
	/* convert a 16-bit number into a 32-bit Linux integer */
	if (num & (1 << 15)) {
		num -= (1 << 16);
	}
	return (num);
}
