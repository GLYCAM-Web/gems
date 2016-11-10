GLYHOME = /home/delaram/Projects/gems/apps/GLYLIB
FLAGS = -L$(GLYHOME)/lib -I$(GLYHOME)/inc -lglylib -Wall -lm
SOURCE = ring_puckering_final.c
OUTEXE = detect_shape

default:
	 gcc $(SOURCE) $(FLAGS) -g -o $(OUTEXE)

gdb:
	gcc $(SOURCE) $(FLAGS) -g -o $(OUTEXE)

eventually:
	gcc test_final.c outputpdb_fromslurp.c $(FLAGS) -g -o $(OUTEXE)

#test:
#       gcc $(TESTIN) $(FLAGS) -g -o testexe
