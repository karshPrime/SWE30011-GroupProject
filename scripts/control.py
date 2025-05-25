
# scripts/control.py

#- Configurable Controls ---------------------------------------------------------------------------

s1_motor = 0
s1_temperature_threshold = 25
old_s1_motor = 0
old_s1_temperature_threshold = 25


#- Public Functions --------------------------------------------------------------------------------

def get_s1_message():
    if s1_motor != old_s1_motor:
        old_s1_motor = s1_motor
        return "m"

    if s1_temperature_threshold != old_s1_temperature_threshold:
        old_s1_temperature_threshold = s1_temperature_threshold
        return f"t{s1_temperature_threshold}"

def clear_s1_message():
    old_s1_temperature_threshold = s1_temperature_threshold
    old_s1_motor = s1_motor

#---------------------------------------------------------------------------------------------------

