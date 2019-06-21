if [ "${GEMSHOME}zzz" == "zzz" ] ; then
	echo "Must set GEMSHOME environment variable.  See docs."
	exit 1
fi
python3 $GEMSHOME/gemsModules/common/transaction.py > schema.json
