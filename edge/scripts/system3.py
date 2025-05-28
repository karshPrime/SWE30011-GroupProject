
# scripts/system3.py

#- Imports -----------------------------------------------------------------------------------------

import time

from .control  import get_s3_data
from .database import database_write3


#- Public Calls ------------------------------------------------------------------------------------

def system_run():
    while True:
        temperature, city, source = get_s3_data()

        if all([temperature, city, source]):
            database_write3(temperature, city, source)

        time.sleep(1)

#---------------------------------------------------------------------------------------------------

