# zoneB_controller.py - SBC-ZoneB (Member 3)
# Cooling with hysteresis + cooling-failure detection.
# RackB-Temp on D1, CRAC-B on D0, Siren on D2 (check your wiring!)

from gpio import *
from time import *

TEST_MODE = True            # True = built-in test temps, False = real sensor
SENSOR, CRAC, SIREN = 1, 0, 2
T_CRIT, T_ON, T_OFF = 35, 27, 22
N_RISE = 5                  # rising loops while cooling = failure
TEST_TEMPS = [20, 24, 28, 29, 30, 31, 32, 33, 31, 25, 21, 36, 30, 25, 20]


def main():
    pinMode(SENSOR, IN)
    pinMode(CRAC, OUT)
    pinMode(SIREN, OUT)
    crac_on, failure, last, rises, n = False, False, None, 0, 0

    while True:
        if TEST_MODE:
            temp = TEST_TEMPS[n % len(TEST_TEMPS)]
        else:
            temp = analogRead(SENSOR) * 100.0 / 1023   # raw 0..1023 -> 0..100 C
        n += 1

        # hysteresis: ON at >=27, OFF at <=22, otherwise hold
        if temp >= T_ON:
            crac_on = True
        elif temp <= T_OFF:
            crac_on = False

        # failure: CRAC on but temp keeps rising
        if crac_on and last is not None and temp > last + 0.2:
            rises += 1
        else:
            rises = 0
        if rises >= N_RISE:
            failure = True
        if temp <= T_OFF:
            failure = False

        status = "COOLING FAILURE" if failure else ("CRITICAL" if temp >= T_CRIT else "OK")
        digitalWrite(CRAC, HIGH if crac_on else LOW)
        customWrite(SIREN, "1" if status != "OK" else "0")
        print("[#%03d] Temp=%.1fC CRAC=%s rises=%d Status=%s" %
              (n, temp, "ON" if crac_on else "OFF", rises, status))

        last = temp
        delay(1000)


if __name__ == "__main__":
    main()