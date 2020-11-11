# Sonew-Bluetooth-Lock-Scripts

F-Secure had an internal competition in March 2020 to hack a bunch of devices. This is my dump of stuff I created to hack one of the targets: Sonew Sonew1fhrxp32ei Bluetooth Pad Lock

![alt text](https://github.com/Yogehi/Sonew-Bluetooth-Lock-Scripts/blob/main/image.PNG)

Amazon page: https://www.amazon.co.uk/gp/product/B07KTSP2VX/ref=ox_sc_act_title_2?smid=A36CCHJKEXVYRD

Repo contents:

* `brute-force-change-password.py` - attempt to change the passcode of the lock via brute force (takes like 8 hours)
* `brute-force-change-physical-code.py` - attempt to change the physical code of the lock via brute force (takes like 2 minutes)
* `brute-force-hidden-command-ef00000000f1.py` - does nothing really, trying to figure out what the hidden command does
* `brute-force-hidden-command-fd00000000fc.py` - does nothing really, trying to figure out what the hidden command does
* `brute-force-send-password.py` - attempt to guess the passcode of the lock via brute force (takes like 8 hours)
* `brute-force-send-physical-code.py` - attempt to guess the physical code of the lock via brute force (takes like 2 minutes)
* `fuzz_new-commands.py` - attempts to fuzz the lock for hidden commands
* `notes.txt` - random notes I took while testing the lock

One day I'll write about how I went about testing this lock.
