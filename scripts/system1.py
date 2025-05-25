
# scripts/system1.py

#- Imports -----------------------------------------------------------------------------------------

import time
import serial

from .control  import clear_s1_message, get_s1_message
from .database import database_write1


#- Public Calls ------------------------------------------------------------------------------------

def Run(port):
    with serial.Serial(port, 9600, timeout=1) as connection:
        time.sleep(2)
        print("[system1] setting up system1")

        while True:
            if connection.in_waiting > 0:
                prompt = connection.readline().decode('utf-8').strip()
                database_write1(prompt)

            message = get_s1_message()
            if message:
                connection.write(message.encode())
                clear_s1_message()

#---------------------------------------------------------------------------------------------------

