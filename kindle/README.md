# Kindle Display

The plan is that the report data will be rendered to an image which will be displayed on a Kindle screen.

Reason for using a Kindle is that the e-ink display seems perfect for data that is not updated very often (plus I have one, rather than buying a e-ink display)

## Notes

There are some complexities with the Kindle. When it goes to sleep the wifi connection is shutdown, so you can't ssh into it to update the image.

This means I will need to setup a script to run using the RTC interrupts on the Kindle. This script will need to start the wifi, then check for a new image on a web server, then update the screen, then go back to sleep.

The same script should run when Kindle is woken up (ie a manual refresh of the display)

Thought would be that all the built in screensavers would be replaced with the data image - this means that whenever the kindle goes to sleep, the image would be displayed

This will require:

- Jailbroken Kindle
- Script to replace build in images with a downloaded image
- BigSpender would need to save the image to a webserver that the Kindle can download from

## Kindle Links

- https://www.instructables.com/Literary-Clock-Made-From-E-reader/
- https://matthealy.com/kindle
- https://www.mobileread.com/forums/showthread.php?t=97636 ()
- https://www.mobileread.com/forums/showthread.php?t=191158 (Kindle 4 Jailbreak)
- https://www.mobileread.com/forums/showthread.php?t=322900 (Run scripts using RTC)
- https://www.mobileread.com/forums/showpost.php?p=3812831&postcount=2 (More RTC stuff)
- https://www.mobileread.com/forums/showthread.php?t=235821&page=3 (More RTC stuff)
