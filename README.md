# RFID-data-management

This uses RFID technology as an identification system. RFID can be used in three instances: access control, record keeping, and attendance keeping. 
All three instances are implemented here.

This is done using **Flask** and **Jinja** to provide the front-end and back-end functionalities.

If a facility is registered using 'Access', access to a place is granted based on your position in the company. Upon registration, RFID tag is set to be have places which it can access.
If a facility is registered using 'Attendance', when the RFID is read, the time is logged and entry or exit is recorded based on what is happening.
If a facility is registered using 'Record', reading of the RFID tag opens up the record pertaining to the RFID tag and it can be updated.

The RFID reading system was implemented using Arduino Uno interfaced with an RFID card reader module and RFID tags. Code was written to the Arduino Uno using Arduino. 
The RFID library used in the code was modified to use display on the RFID tag number when it is read. This is communicated to Python codebase using serial connection made possible by the **pyserial** library.
