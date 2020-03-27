#!/bash/bin

usage() {
	cat << USAGE >&2


Usage: bash logs/clearLogs.sh LOGNAME

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
	echo "" > ./logs/git-ignore-me_gemsDebug.log
	echo "" > ./logs/git-ignore-me_gemsInfo.log
	echo "" > ./logs/git-ignore-me_gemsError.log
fi

if [ "$1" == "debug" ]; then
	echo "" > ./logs/git-ignore-me_gemsDebug.log
fi

if [ "$1" == "info" ]; then
	echo "" > ./logs/git-ignore-me_gemsInfo.log
fi

if [ "$1" == "error" ]; then
	echo "" > ./logs/git-ignore-gemsError.log
fi

exit 0