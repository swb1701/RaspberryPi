Read and push dB meter data to the cloud.

For auto startup place soundmeter in

/etc/init.d/soundmeter

and run "update-rc.d soundmeter defaults"

Sound meter needs privileges to access usb and
the python-requests package should be installed
for the cloud push operation shown in the code.
