#!/bin/bash

# clear the prior file
echo "" > /home/lldp/kj_LEFT.txt

if [[ $(ifplugstatus eth0 | grep 'link beat detected') ]];
 then 
  IPADDR="`ifconfig eth0 | awk '/inet addr/ {print substr($2,6)\"\n\"substr($4,6)}'`"
  if [[ "$IPADDR" == "" ]];
    then IPADDR="NO DHCP\nIP ADDRESS"
  fi
  echo -e "$IPADDR" > /home/lldp/kj_LEFT.txt
 else
  echo -e 'Dammit, Jim...\neth0 unplugged' > /home/lldp/kj_LEFT.txt
fi

