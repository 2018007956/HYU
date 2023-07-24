        nor 0 0 1 reg1 is -1
        add 0 1 2 reg2 is -1
        lw 0 3 ten reg3 is 10
        lw 0 4 five reg4 is 5
        jalr 3 6 reg6 is 5
branch  beq 0 0 2 go to jump
        add 1 1 1
        add 1 1 1
jump    noop
        halt
        jalr 6 7 go to branch
one     .fill 1
ten     .fill 10
five    .fill 5