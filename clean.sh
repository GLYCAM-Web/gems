TARGET_MAKE_FILE="Makefile"
echo $TARGET_MAKE_FILE
cd gmml
if [ -f $TARGET_MAKE_FILE ]; then
	make -f $TARGET_MAKE_FILE distclean
	rm -rf gmml.pro*
else
	make distclean
	rm -rf gmml.pro*
fi
cd ..
rm -rf gmml_wrap.cxx gmml_wrap.o gmml.py gmml.pyc _gmml.so
