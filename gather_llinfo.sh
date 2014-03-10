#!/bin/bash

# clear the text file of stale information
echo "" > /home/lldp/kj_DOWN.txt

if [[ $(ifplugstatus eth0 | grep 'link beat detected') ]];
 then
# Based on HP ProCurve LLDP and Cisco CDP output, gather select information for LCD display
  LLINFO_SWITCH="`lldpctl -f keyvalue | awk -F\"=\" '/chassis.name/ {print \$NF}'`"
  LLINFO_PORT="`lldpctl -f keyvalue | awk -F\"=\" '/port.descr/ {print \$NF}' | sed -r -e 's/Ten//i; s/GigabitEthernet//i; s/FastEthernet//i; s/Ethernet//i; s/Not received//i'`"
  LLINFO_VLAN="`lldpctl -f keyvalue | awk -F\"=\" '/vlan-id/ {print \$NF}'`"

  if [ "$LLINFO_PORT" == "" ]
   then
    LINE1="No useful LLDP"
    LINE2="Press to retry"
   else
    LINE1="${LLINFO_SWITCH}"
    LINE2="P:${LLINFO_PORT} V:${LLINFO_VLAN}"
  fi

  echo -e "${LINE1}\n${LINE2}" > /home/lldp/kj_DOWN.txt

 else
  echo -e 'Dammit, Jim...\neth0 unplugged' > /home/lldp/kj_DOWN.txt
fi


#echo $LINE1
#echo $LINE2

# 16 characters wide
# echo "0123456789ABCDEF"
