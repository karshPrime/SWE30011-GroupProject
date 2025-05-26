
# scripts/control.py

#- Configurable Controls ---------------------------------------------------------------------------

s1_motor = 0
s1_temperature_threshold = 25
s2_moisture_threshold = 20
s3_temperature = ""

old_s1_motor = 0
old_s1_temperature_threshold = 25
old_s3_temperature = ""


#- Public Functions --------------------------------------------------------------------------------

def get_s1_message():
    global s1_motor
    global old_s1_motor

    if s1_motor != old_s1_motor:
        old_s1_motor = s1_motor
        return "m"

    global s1_temperature_threshold
    global old_s1_temperature_threshold

    if s1_temperature_threshold != old_s1_temperature_threshold:
        old_s1_temperature_threshold = s1_temperature_threshold
        return f"t{s1_temperature_threshold}"


def clear_s1_message():
    global s1_temperature_threshold
    global old_s1_temperature_threshold

    old_s1_temperature_threshold = s1_temperature_threshold
    old_s1_motor = s1_motor


def get_s2_moisture_threshold():
    return s2_moisture_threshold


def get_s3_message():
    global s3_temperature
    global old_s3_temperature

    if s3_temperature != old_s3_temperature:
        old_s3_temperature = s3_temperature
        return s3_temperature


#---------------------------------------------------------------------------------------------------

