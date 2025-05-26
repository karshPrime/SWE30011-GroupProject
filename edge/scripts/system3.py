
# scripts/system3.py

#- Imports -----------------------------------------------------------------------------------------

import time

from .control  import get_s3_data
from .database import database_write3


#- Public Calls ------------------------------------------------------------------------------------

def Run():
    while True:
        button, temperature, motionSensor = get_s3_data()

        if all(x is not None for x in (button, temperature, motionSensor)):
            database_write3(button, temperature, motionSensor)

        time.sleep(1)

#---------------------------------------------------------------------------------------------------

