cd gmml
make clean
#make distclean
#rm -rf gmml.pro*
#qmake -project -t lib
#qmake -o
make 
cd ..
swig -c++ -python gmml.i
g++ -O2 -fPIC -c gmml_wrap.cxx -I/usr/include/python2.7
g++ -shared gmml/*.o gmml_wrap.o -o _gmml.so


