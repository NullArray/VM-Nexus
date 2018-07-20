#!/bin/bash

# QEMU optional supporting libs
function pkgs(){
	
	sudo apt-get install            \
		libaio-dev 		\
		libbluetooth-dev	\
		libbrlapi-dev 		\
		libbz2-dev		\
		libcap-dev 		\
		libcap-ng-dev 		\
		libcurl4-gnutls-dev 	\
		libgtk-3-dev		\
		libibverbs-dev 		\
		libjpeg8-dev 		\
		libncurses5-dev 	\
		libnuma-dev		\
		librbd-dev		\
		librdmacm-dev		\
		libsasl2-dev 		\
		libsdl1.2-dev 		\
		libseccomp-dev 		\
		libsnappy-dev 		\
		libssh2-1-dev		\
		libvde-dev 		\
		libvdeplug-dev 		\
		libxen-dev 		\
		liblzo2-dev 		\
		xfslibs-dev		\
		valgrind
		
	echo -e "\nRunning updates...\n" && sleep 3
	sudo apt-get update && sudo apt-get upgrade
	
	clear && echo "Done"
}

if [[ "$EUID" -ne 0 ]]; then
   echo -e "\nPlease run this script as root\n"
else
	read -p "Install optional supporting QEMU libs? [Y/n]: " choice
	if [[ $choice == 'y' || $choice == 'Y' ]]; then
		pkgs
	else
		echo -e "\nAborted\n"
	fi
fi
