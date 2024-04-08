
# Fortran compiler: gfortran, g77, ifort, pgf77...
FC = gfortran
FLAGS =

OBJS= resp.o  
SRCS= resp.f

resp:	$(OBJS) 
	$(FC) $(FLAGS) $(OBJS) -o resp

clean:
	rm -rf $(OBJS) resp

