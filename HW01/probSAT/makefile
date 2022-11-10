CC=gcc
CFLAGS= -Wall -Wextra -static -O3 -funroll-loops -fexpensive-optimizations
PROGS=probSAT

all: $(PROGS)
probSAT: probSAT.o xoshiro256plus.o rngctrl.o
		 $(CC) $(CFLAGS) probSAT.o xoshiro256plus.o rngctrl.o -lm -o probSAT

probSAT.o::  rngctrl.h xoshiro256plus.h
rngctrl.o:: rngctrl.h xoshiro256plus.h
xoshiro256plus.o:: xoshiro256plus.h

clean:
	- rm *.o *.log ${PROGS}

