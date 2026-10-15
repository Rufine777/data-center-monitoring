# Zone B Pin Map: SBC-ZoneB

Source: `zoneB_controller.py` (Member 3). Cooling control with hysteresis and cooling-failure detection.

## Pin assignments

| Pin | Constant | Device | Direction | Signal | Access in code |
|-----|----------|--------|-----------|--------|----------------|
| D0 | `CRAC = 0` | CRAC-B (cooling unit) | OUT | Digital, HIGH = ON, LOW = OFF | `digitalWrite(CRAC, ...)` |
| D1 | `SENSOR = 1` | RackB-Temp (temperature sensor) | IN | Analog, raw 0..1023 scaled to 0..100 C | `analogRead(SENSOR)` |
| D2 | `SIREN = 2` | Siren (alarm) | OUT | Custom write, "1" = alarm, "0" = silent | `customWrite(SIREN, ...)` |

## Thresholds

| Name | Value | Meaning |
|------|-------|---------|
| `T_ON` | 27 C | CRAC turns ON at or above this temperature |
| `T_OFF` | 22 C | CRAC turns OFF at or below this temperature (holds state in between) |
| `T_CRIT` | 35 C | Status becomes CRITICAL at or above this temperature |
| `N_RISE` | 5 loops | Consecutive rising readings while the CRAC is ON before COOLING FAILURE is declared |

A reading counts as rising when it is more than 0.2 C above the previous one. A failure latches until the temperature falls to `T_OFF` or below.

## Siren logic

| Status | Condition | Siren (D2) |
|--------|-----------|------------|
| OK | None of the conditions below | `"0"` |
| CRITICAL | Temp >= 35 C | `"1"` |
| COOLING FAILURE | CRAC on and 5 rising loops in a row | `"1"` |

COOLING FAILURE takes priority over CRITICAL in the printed status.

## Test mode

`TEST_MODE = True` replaces the sensor with a built-in sequence, so D1 is not read:

`20, 24, 28, 29, 30, 31, 32, 33, 31, 25, 21, 36, 30, 25, 20` (one value per 1 s loop, repeating)

Set `TEST_MODE = False` to read the real sensor on D1.

## To verify on the .pkt

- The script header says "check your wiring". The pin numbers above come from the code only, not from the topology.
- Confirm that RackB-Temp, CRAC-B and the siren are physically connected to D1, D0 and D2 on SBC-ZoneB.
- Confirm that the sensor uses an analog pin the SBC's `analogRead` can address.
