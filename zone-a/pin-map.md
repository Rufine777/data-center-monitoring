# Pin map: SBC-ZoneA (Member 2)

Controller: **SBC-ZoneA**, `192.168.20.20/24`, gateway `192.168.20.1` (VLAN 20, Access-SW2).

The sensor and cooler connect to the SBC with the **IoT Custom Cable**. They have no IP address and no switch port.

| Device | Device-side port | SBC pin (used in script) | Direction | Script setting | Read/write call |
|---|---|---|---|---|---|
| RackA-Temp (Temperature Sensor) | A0 | **D1** | Input | `SENSOR_PIN = 1` | `analogRead(1)` |
| CRAC-A (Air Cooler) | D0 | **D0** | Output | `CRAC_PIN = 0` | `digitalWrite(0, HIGH/LOW)` |

## Verification
- CRAC-A on D0: **verified.** The cooler visibly switched on and off in Packet Tracer when the script wrote to pin 0.
- RackA-Temp on D1: **verified.** `analogRead(1)` returned changing values (for example raw 160-164). Reading pin 0 gave 0, which is how the wrong pin was found.

## Sensor conversion
Raw reading to °C: `C = raw x 100 / 1023` (0-1023 mapped to 0-100 °C). This mapping is an **assumption** and was not verified against a reference temperature.

## Cooler states
| State | Meaning | `digitalWrite` value |
|---|---|---|
| OFF | Temp <= 22 °C | `LOW` |
| ON | Temp >= 27 °C | `HIGH` |
| HIGH | Temp >= 35 °C (CRITICAL) | `HIGH` (same pin; `USE_ANALOG = True` gives separate levels) |

With `USE_ANALOG = False` ON and HIGH both write `HIGH`, because the cooler has one digital input. They differ only in the printed state and the status message.

## How the pins were found
Hovered over the SBC end of each cable to read the port name. (The SBC **Config** tab does not list pins.)