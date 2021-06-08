# Makefile for GlycoProtein Builder
# Created by Davis Templeton 2018-07-23

CC = g++
CFLAGS = -std=c++0x -I ${GEMSHOME}/gmml/includes/ -I includes/
RFLAGS = -Wl,-rpath,${GEMSHOME}/gmml/lib/
LFLAGS = -I${GEMSHOME}/gmml/includes/ -L${GEMSHOME}/gmml/lib/ -lgmml
COMPILE = $(CC) $(CFLAGS) -c
LINK = $(LFLAGS)
RUNTIME = $(RFLAGS)
DEBUG = -g 2
RM = rm -f

SRC = ./src
INC = ./includes
BUILD = ./build
BIN = ./bin

all: $(BIN)/gp_builder $(BUILD)/bead_residues.o $(BUILD)/genetic_algorithm.o $(BUILD)/glycoprotein_builder.o $(BUILD)/glycosylationsite.o $(BUILD)/io.o $(BUILD)/main.o $(BUILD)/overlap_record.o $(BUILD)/resolve_overlaps.o $(BUILD)/selections.o

$(BIN)/gp_builder: $(BUILD)/main.o $(BUILD)/bead_residues.o $(BUILD)/genetic_algorithm.o $(BUILD)/glycoprotein_builder.o $(BUILD)/glycosylationsite.o $(BUILD)/io.o $(BUILD)/overlap_record.o $(BUILD)/resolve_overlaps.o $(BUILD)/selections.o
	$(CC) $(BUILD)/main.o $(BUILD)/bead_residues.o $(BUILD)/genetic_algorithm.o $(BUILD)/glycoprotein_builder.o $(BUILD)/glycosylationsite.o $(BUILD)/io.o $(BUILD)/overlap_record.o $(BUILD)/resolve_overlaps.o $(BUILD)/selections.o $(LINK) $(RUNTIME) -o $(BIN)/gp_builder

$(BUILD)/main.o: $(SRC)/main.cpp $(INC)/io.h $(INC)/resolve_overlaps.h $(INC)/bead_residues.h $(INC)/genetic_algorithm.h $(INC)/glycoprotein_builder.h
	$(COMPILE) $(SRC)/main.cpp -o $(BUILD)/main.o

$(BUILD)/bead_residues.o: $(SRC)/bead_residues.cpp $(INC)/glycosylationsite.h $(INC)/selections.h
	$(COMPILE) $(SRC)/bead_residues.cpp -o $(BUILD)/bead_residues.o

$(BUILD)/genetic_algorithm.o: $(SRC)/genetic_algorithm.cpp $(INC)/genetic_algorithm.h $(INC)/bead_residues.h
	$(COMPILE) $(SRC)/genetic_algorithm.cpp -o $(BUILD)/genetic_algorithm.o

$(BUILD)/glycoprotein_builder.o: $(SRC)/glycoprotein_builder.cpp $(INC)/glycoprotein_builder.h $(INC)/io.h $(INC)/glycosylationsite.h
	$(COMPILE) $(SRC)/glycoprotein_builder.cpp -o $(BUILD)/glycoprotein_builder.o

$(BUILD)/glycosylationsite.o: $(SRC)/glycosylationsite.cpp $(INC)/glycosylationsite.h $(INC)/overlap_record.h
	$(COMPILE) $(SRC)/glycosylationsite.cpp -o $(BUILD)/glycosylationsite.o

$(BUILD)/io.o: $(SRC)/io.cpp $(INC)/io.h
	$(COMPILE) $(SRC)/io.cpp -o $(BUILD)/io.o

$(BUILD)/overlap_record.o: $(SRC)/overlap_record.cpp $(INC)/overlap_record.h
	$(COMPILE) $(SRC)/overlap_record.cpp -o $(BUILD)/overlap_record.o

$(BUILD)/resolve_overlaps.o: $(SRC)/resolve_overlaps.cpp $(INC)/resolve_overlaps.h $(INC)/bead_residues.h $(INC)/glycosylationsite.h $(INC)/glycoprotein_builder.h $(INC)/metropolis_criterion.h
	$(COMPILE) $(SRC)/resolve_overlaps.cpp -o $(BUILD)/resolve_overlaps.o

$(BUILD)/selections.o: $(SRC)/selections.cpp $(INC)/selections.h
	$(COMPILE) $(SRC)/selections.cpp -o $(BUILD)/selections.o

clean:
	$(RM) $(BUILD)/*.o
	$(RM) $(BIN)/gp_builder
