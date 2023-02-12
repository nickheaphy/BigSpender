#!/bin/sh

# most of this code is from https://www.mobileread.com/forums/showthread.php?t=236104

do_cmd() {

    DISABLE_WIFI=0
    TEST_DOMAIN="192.168.1.10"
    NETWORK_TIMEOUT=30
    IMAGE_URI="http://192.168.1.10:8082/report.png"
    IMAGE_SAVE="report.png"

    # enable wireless if it is currently off
    if [ 0 -eq `lipc-get-prop com.lab126.cmd wirelessEnable` ]; then
        logger "WiFi is off, turning it on now"
        lipc-set-prop com.lab126.cmd wirelessEnable 1
        DISABLE_WIFI=1
    fi

    # wait for network to be up
    TIMER=${NETWORK_TIMEOUT}     # number of seconds to attempt a connection
    CONNECTED=0                  # whether we are currently connected
    while [ 0 -eq $CONNECTED ]; do
        # test whether we can ping outside
        /bin/ping -c 1 -w 2 $TEST_DOMAIN > /dev/null && CONNECTED=1

        # if we can't, checkout timeout or sleep for 1s
        if [ 0 -eq $CONNECTED ]; then
            TIMER=$(($TIMER-1))
            if [ 0 -eq $TIMER ]; then
                logger "No internet connection after ${NETWORK_TIMEOUT} seconds, aborting."
                break
            else
                sleep 1
            fi
        fi
    done

    if [ 1 -eq $CONNECTED ]; then
        if curl -s --fail $IMAGE_URI -o $IMAGE_SAVE > /dev/null; then

            # refresh screen
            logger "Updating image on screen"
            eips -c
            eips -c
            eips -g $IMAGE_SAVE
            
        else
            logger "Error updating screensaver"
        fi
    fi

    # disable wireless if necessary
    if [ 1 -eq $DISABLE_WIFI ]; then
        logger "Disabling WiFi"
        lipc-set-prop com.lab126.cmd wirelessEnable 0
    fi

	# set picture using fbink or eips
    # enable the wifi
    # lipc-set-prop com.lab126.cmd wirelessEnable 1
    # # download the image
    # if curl --fail http://192.168.1.10:8082/report.png -o report.png; then
    #     eips -c
    #     eips -c
    #     eips -g report.png
    # else
    #     # …(failure)
    #     # do nothing
    #     logger "Could not download image";
    # fi
    # # disable the wifi
    # lipc-set-prop com.lab126.cmd wirelessEnable 0
}

run_cmd() {
	do_cmd()
	# set to your delay between picture changes
    # offset is in seconds ie 7200 = 2hr
	DELTA=$(( `date +%s` + 7200 ))
	lipc-set-prop -i  com.lab126.powerd rtcWakeup $DELTA
}

# Main
case "${1}" in
	"run_cmd" )
		${1}
	;;
	"do_cmd" )
		${1}
	;;
	* )
		run_cmd
	;;
esac

return 0