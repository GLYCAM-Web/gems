#!/bash/bin

usage() {
	cat << USAGE >&2


Usage: bash clearLogs.sh LOGNAME

	LOGNAME: Target logfile or ALL. Default to ALL
		error
		info
		debug

Example: 

	bash clearLogs.sh error

Clears the error log file.


USAGE
	exit 1
}

if [ "$1" == "help" ]; then
	usage
fi

if [ "$1" == "" ]; then
	echo "" > git-ignore-me_gemsDebug.log
	echo "" > git-ignore-me_gemsInfo.log
	echo "" > git-ignore-me_gemsError.log
fi

if [ "$1" == "debug" ]; then
	echo "" > git-ignore-me_gemsDebug.log
fi

if [ "$1" == "info" ]; then
	echo "" > git-ignore-me_gemsInfo.log
fi

if [ "$1" == "error" ]; then
	echo "" > git-ignore-gemsError.log
fi

exit 0