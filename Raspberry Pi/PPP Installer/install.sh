#!/bin/sh

YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[1;34m'
SET='\033[0m'

apt-get update
apt-get install ppp tmux screen putty ufw -y

mv chat-connect /etc/chatscripts/
mv chat-disconnect /etc/chatscripts/

mkdir -p /etc/ppp/peers
mv provider /etc/ppp/peers/provider

if ! (grep -q 'route' /etc/ppp/ip-up ); then
    echo "sudo route del default" >> /etc/ppp/ip-up
    echo "sudo route add default ppp0" >> /etc/ppp/ip-up
fi

mv reconnect.sh /usr/src/
chmod +x /usr/src/reconnect.h
mv nbiot.service /etc/systemd/system/
			  
systemctl daemon-reload
systemctl enable nbiot.service
# sudo pon # to go online for NBIOT modem
# sudo poff # to go offline for NBIOT modem

echo "${YELLOW}To connect to NBIOT modem run ${BLUE}\"sudo pon\"${YELLOW} and to disconnect run ${BLUE}\"sudo poff\" ${SET}"
echo "${YELLOW}To Run as Service ${BLUE}\"sudo systemctl enable nbiot.service\" ${SET}"

read -p "Press ENTER key to reboot" ENTER
reboot