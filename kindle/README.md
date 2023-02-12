# Kindle Display

The plan is that the report data will be rendered to an image which will be displayed on a Kindle screen.

Reason for using a Kindle is that the e-ink display seems perfect for data that is not updated very often (plus I have one, rather than buying a e-ink display)

This is all bodged together from other projects! See links below

## Notes

There are some complexities with the Kindle. When it goes to sleep the wifi connection is shutdown, so you can't ssh into it to update the image.

This means I will need to setup a script to run using the RTC interrupts on the Kindle. This script will need to start the wifi, then check for a new image on a web server, then update the screen, then go back to sleep.

The same script should run when Kindle is woken up (ie a manual refresh of the display)

Thought would be that all the built in screensavers would be replaced with the data image - this means that whenever the kindle goes to sleep, the image would be displayed

This will require:

- Jailbroken Kindle
- Script to replace build in images with a downloaded image
- BigSpender would need to save the image to a webserver that the Kindle can download from

## Installation

First you need to jailbreak your Kindle (the following is for my Kindle 4 non-touch model)

Next up is to access the Kindle via the command line so we can set up our script to download images. First, we need to enable USBNetwork to allow command-line access via USB:

- Disconnect your Kindle from your computer
- Press the keyboard button on the Kindle, and type `;debugOn` (make sure to get the semicolon at the beginning), and then enter (↵) to enable debug mode.
- Press the keyboard button again, and type `~usbNetwork` and hit enter (↵). It may pause for a second. Once it’s done, press keyboard, type `;debugOff` and hit enter.
- Reconnect your Kindle to your computer via USB.

From a command line on your computer (i.e. in the Terminal app on a Mac):

Type `ssh root@192.168.15.244` and hit enter.

You’ll be prompted for a password. The default password is `mario`.

You’re in! One more thing before we can do anything: by default, the Kindle’s drive is mounted in read-only mode. To make it writeable, type `mntroot rw` and hit enter.

Create the image-downloading script `dlreport.sh` and `setup_rtc.sh`

Run the `setup_rtc.sh` as a background script (use `&`)

## Hosting the image

Edit the `credentials.py` to include the scp details of the server to copy the image to.



## Kindle Links

- https://www.instructables.com/Literary-Clock-Made-From-E-reader/
- https://matthealy.com/kindle
- https://www.mobileread.com/forums/showthread.php?t=97636 ()
- https://www.mobileread.com/forums/showthread.php?t=191158 (Kindle 4 Jailbreak)
- https://www.mobileread.com/forums/showthread.php?t=322900 (Run scripts using RTC)
- https://www.mobileread.com/forums/showpost.php?p=3812831&postcount=2 (More RTC stuff)
- https://www.mobileread.com/forums/showthread.php?t=235821&page=3 (More RTC stuff)
- https://www.mobileread.com/forums/showthread.php?t=236104 (Screensaver)
- https://www.mobileread.com/forums/showthread.php?t=236104&page=5 (wake and enable wifi)