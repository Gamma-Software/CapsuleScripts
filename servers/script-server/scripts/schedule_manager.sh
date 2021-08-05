#!/bin/sh

ACTION=${1}
FILE_RAW=${2}
FILE=$(echo $FILE_RAW | sed 's/ /\ /g') #Strips spaces from filenames, posix doesn't like that.

case ${ACTION} in
list)
COMMAND="cat"
;;
delete)
COMMAND="rm"
;;
*)
printf "$red" "Invalid option, please choose list/delete"
esac

printf "Okay, running ${COMMAND} on the selected file: ${FILE}"
printf "\n\n"
${COMMAND} "${FILE}"
service script_server restart