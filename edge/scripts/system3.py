
# scripts/system3.py

#- Imports -----------------------------------------------------------------------------------------

import time
import serial

from .control import get_s3_message
from .database import database_write3


#- Public Calls ------------------------------------------------------------------------------------

def Run():
    with serial.Serial( port, 9600, timeout=1 ) as connection:
        time.sleep( 2 )
        print( "[system3] setting up system3" )

        while True:
            # --- Prepare message from control ---
            message = get_s3_message()
            if message:
                connection.write(message.encode('utf-8') + b'\n')

            # --- Read response from Arduino ---
            if connection.in_waiting > 0:
                line = connection.readline().decode('utf-8').strip()

                # Expecting something like: PM:1;BT:0;MS:2;
                if line.startswith("PM:"):
                    try:
                        parts = line.split(";")
                        pm = int(parts[0].split(":")[1])
                        bt = int(parts[1].split(":")[1])
                        ms = int(parts[2].split(":")[1])
                        print( "[system3] ", pm, bt, ms )
                        database_write3(pm, bt, ms)

                    except Exception as e:
                        print(f"[system3] Failed to parse or write data: {e}")

            time.sleep(1)

