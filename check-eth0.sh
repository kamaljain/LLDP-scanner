#!/bin/bash
#
# check eth0 link status, if it's unplugged - restart lldpd to flush cached info

while true
 do
    ifplugstatus eth0 | grep "unplugged"
    if [[ $? -ne 1 ]]
     then
#	ifdown eth0 && ifup eth0
	/etc/init.d/lldpd restart
     else
	sleep 1
    fi
 done

