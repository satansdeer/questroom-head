#!/bin/bash

if [ -z $1 ]; then
    exit 1
fi
search_pattern=$1
output_result=""

# echo "search_pattern: $search_pattern"
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        syspath="${sysdevpath%/dev}"
        devname="$(udevadm info -q name -p $syspath)"
        [[ "$devname" == "bus/"* ]] && continue
        eval "$(udevadm info -q property --export -p $syspath)"
        [[ -z "$ID_SERIAL" ]] && continue

        format_device="/dev/$devname - $ID_SERIAL"
         # echo "format_device: $format_device"
        result=`echo $format_device | awk -v search=$search_pattern '{if ($0 ~ search) print $1}'`
        if [ ! -z $result ]; then
            echo -n $result
            exit
        fi
    )
done
