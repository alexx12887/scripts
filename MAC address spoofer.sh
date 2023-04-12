#!/bin/bash

if [ $(id -u) != "0" ]; then

	echo "[-] Please run as root"

	exit 0

fi

OG_MAC_ADDR=$(ifconfig en0 | grep ether)
OG_MAC_ADDR=${OG_MAC_ADDR//	ether /}

echo "[*] Orginal MAC address: $OG_MAC_ADDR"

A=$(openssl rand -hex 1)
B=$(openssl rand -hex 1)
C=$(openssl rand -hex 1)
D=$(openssl rand -hex 1)
E=$(openssl rand -hex 1)
F=$(openssl rand -hex 1)

RAND_MAC_ADDR="$A:$B:$C:$D:$E:$F"

echo "[*] New MAC address: $RAND_MAC_ADDR"

sudo airport -z

echo "[*] Disassociating from any network"

sleep 1

echo "[*] Changing MAC address on en0"

sudo ifconfig en0 ether $RAND_MAC_ADDR

sleep 2

echo "[*] Reconnecting WIFI"

sudo ifconfig en0 down

sleep 1

sudo ifconfig en0 up

CHECK_IF_CHANGED=$(ifconfig en0 | grep ether)
CHECK_IF_CHANGED=${CHECK_IF_CHANGED//ether /}

if [[ $CHECK_IF_CHANGED == *"$RAND_MAC_ADDR"* ]]; then

	echo "[+] MAC address successfully changed from ${OG_MAC_ADDR}to $RAND_MAC_ADDR"

else

	echo "[-] MAC address change failed"

fi
