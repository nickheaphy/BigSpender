#!/bin/sh

# https://www.mobileread.com/forums/showpost.php?p=3812831&postcount=2
# Run this on the kindle to setup the RTC so it displays a picture.
# Reason for doing this is that the only time you can program the RTC using 
# lipc-set-prop -i  com.lab126.powerd rtcWakeup 100
# is when the kindle is in the readyToSuspend state which it enters for a few seconds before sleeping.

# The idea is that you run this, then leave the kindle so it enters readyToSuspend then the
# script sets up the RTC to call your program. 

# location of your program
PROGRAM=/mnt/us/dlreport.sh
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8


do_program()
{
	if [[ -f "$PROGRAM" ]]; then
	  # run program function to set picture
	  $PROGRAM do_cmd
	fi
}

run_program()
{
	if [[ -f "$PROGRAM" ]]; then
	  # run program function to reset wakup rtc
	  $PROGRAM run_cmd
	fi
}

lipc-wait-event -m com.lab126.powerd goingToScreenSaver,readyToSuspend | while read event; do
	case "$event" in
		goingToScreenSaver*)
			do_program;;
		readyToSuspend*)
			run_program;
	esac
done;