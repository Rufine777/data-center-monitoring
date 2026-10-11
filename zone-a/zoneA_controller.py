# zoneA_controller.py  -  SBC-Zone A cooling controller (Member 2)
# Paste into SBC-Zone A > Programming > main.py
#
# Tiered cooling with hysteresis:
#   Temp >= 35 C        -> CRAC HIGH + status CRITICAL
#   Temp >= 27 C        -> CRAC ON
#   Temp <= 22 C        -> CRAC OFF
#   22 C < Temp < 27 C  -> hold the previous state

from gpio import *
from time import *

# ---------------- SETTINGS (edit these) ----------------
TEST_MODE   = True    # True = use TEST_TEMPS below, False = read the real sensor
SENSOR_PIN  = 0       # pin RackA-Temp is wired to (check SBC Config tab)
CRAC_PIN    = 0       # pin CRAC-A is wired to (check SBC Config tab)
USE_ANALOG  = False   # False = digitalWrite on/off; True = analogWrite levels
DELAY_MS    = 1000    # time between readings

# Calibration: temp_c = (raw - RAW_AT_LOW) * SCALE + C_AT_LOW
# Default assumes the sensor already reports degrees C (raw = C).
# After you measure two (raw, C) pairs, set these. Example for 0..1023 -> 0..100 C:
#   RAW_AT_LOW = 0, C_AT_LOW = 0, SCALE = 100.0 / 1023
RAW_AT_LOW  = 0
C_AT_LOW    = 0
SCALE       = 1.0

# Thresholds
T_CRITICAL = 35
T_ON       = 27
T_OFF      = 22

# Test sequence that exercises every branch of the hysteresis
TEST_TEMPS = [20, 24, 28, 25, 21, 36, 30, 25, 20]

OFF, ON, HIGH_STATE = 0, 1, 2
STATE_NAMES = ["OFF", "ON", "HIGH"]


def calibrate(raw):
    """Convert the raw sensor reading to degrees C."""
    return (raw - RAW_AT_LOW) * SCALE + C_AT_LOW


def read_temp(step):
    if TEST_MODE:
        return TEST_TEMPS[step % len(TEST_TEMPS)]
    raw = analogRead(SENSOR_PIN)
    print("raw = " + str(raw))          # keep for calibration checks
    return calibrate(raw)


def set_crac(state):
    if USE_ANALOG:
        levels = [0, 512, 1023]
        analogWrite(CRAC_PIN, levels[state])
    else:
        digitalWrite(CRAC_PIN, LOW if state == OFF else HIGH)


def next_state(temp, state):
    """Hysteresis logic. Returns (new_state, status_text)."""
    if temp >= T_CRITICAL:
        return HIGH_STATE, "CRITICAL"
    if temp >= T_ON:
        return ON, "NORMAL"
    if temp <= T_OFF:
        return OFF, "NORMAL"
    return state, "NORMAL"              # between thresholds: hold


def main():
    if not TEST_MODE:
        pinMode(SENSOR_PIN, IN)
    pinMode(CRAC_PIN, OUT)

    state = OFF
    set_crac(state)
    count = 0
    print("Zone A controller started (TEST_MODE=" + str(TEST_MODE) + ")")

    while True:
        count += 1
        temp = read_temp(count - 1)
        new_state, status = next_state(temp, state)
        changed = "CHANGED" if new_state != state else "held"
        if new_state != state:
            set_crac(new_state)
        state = new_state
        print("[#%03d] Temp=%.1fC  CRAC=%s (%s)  Status=%s"
              % (count, temp, STATE_NAMES[state], changed, status))
        delay(DELAY_MS)


if __name__ == "__main__":
    main()
