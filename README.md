# blescanner
Bluethooth Beacan Scanner for Raspberry Pi and Hubitat Presence 


to use this, do the following:

Grab a raspberry Pi, any model should work fine, I used a Rpi model 2 because it was laying around.
Grab a bluetooth dongle if your pi doesn't have it, I used this one:
https://www.amazon.com/dp/B009ZIILLI/ref=cm_sw_em_r_mt_dp_U_J8FkEbD7YM324
Grab a beacon or 2, I use these:
https://www.amazon.com/gp/product/B07FC5FMHW/ref=ppx_yo_dt_b_asin_title_o06_s01

-------

Setup the Pi, I won't go into this deeply, I just grabbed Buster from the raspian site.
I did a very minimal install, with only the base packages and SSH

Install the Bluz bluetooth stack, I followed this guide:
https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation

Grab the files here: https://github.com/switchdoclabs/iBeacon-Scanner-
and drop them in a folder with the beaconsensor.py file on your pi, I used /usr/local/bin/blescanner
(I used that path for access later to run as a service)

you'll need to install the Maker API app on your hubitat, and capture some details from that page to put in this script
(the application ID and Token specifically)

you'll need to setup a virtual presence sensor for each beacon you want to scan for, and allow Maker to control them.

back on the Pi, you'll need to find your beacon information,
I use the eddystone app on my phone to change the beacon name so it was easier to find.
then run "hcitool lescan" which should crank out MAC addresses and names of everything it can see.
you'll put that MAC address, in lower case, in the script along with a pretty name, and hubitat device ID for
the virtual presence sensor you created earlier.

Then give it a run and it should output to the command line and /var/log/blescanner.log what's going on and if all is working.

There's provisions in the script for 3 beacons, but more can easily be added, or some removed, by updateing the list.

Once you get it running properly on the command line, you can make it a service by following this guide:
http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

then, reboot your pi and make sure it started fine and works. I did testing by turning beacons on and off.

once that's done, toss the beacons in your cars and enjoy!

you may need to play around with where the raspberry pi sits in relation to the beacons when they're home. I have mine under
a second floor window above my garage door, so it can see beacons in the driveway and garage.

Thanks to Dane Troyer and his original guide that I followed and augmented, available here:
https://medium.com/@troyerdane/accurate-and-reliable-presence-detection-using-ble-b54e95d7d8bd
also Big thanks to the original author of the blescan.py app, John Shovic of Switchdoclabs.
