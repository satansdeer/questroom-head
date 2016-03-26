#!/bin/bash

search_pattern=$1
output_result=""

for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        syspath="${sysdevpath%/dev}"
        devname="$(udevadm info -q name -p $syspath)"
        [[ "$devname" == "bus/"* ]] && continue
        eval "$(udevadm info -q property --export -p $syspath)"
        [[ -z "$ID_SERIAL" ]] && continue

        format_device="/dev/$devname - $ID_SERIAL"
        # echo $format_device
        result=`echo $format_device | awk -v search="$search_pattern" '{if ($0 ~ search) print $1}'`
        if [ ! -z $result ]; then
            echo $result
            exit
        fi
    )
done
