        beq 0 0 7
        noop
        noop
        noop
        noop
        noop
        noop
        halt end of program
        nor 0 0 1
        add 1 1 2
        add 2 2 2
        add 2 2 2
        nor 0 2 2 reg2 is 7
        add 2 1 3 reg3 is 6
        add 3 3 3 reg3 is 12
        add 3 3 3 reg3 is 24
        sw 3 2 -5
        lw 0 4 seven
        jalr 4 5 go to end of program
seven   .fill 2147483647 will become 7