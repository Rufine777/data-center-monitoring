# Data Center Environmental Monitoring & Automated Cooling

Cisco Packet Tracer project (team of 4). A small simulated data center that monitors temperature, humidity, smoke and water leaks, and automatically controls cooling and alarms on a segmented, secured network.

**Design targets** (typical data center ranges, cite ASHRAE in the report): temperature 18-27 °C, humidity 40-60 %.

## Team

| Member | Role | Folder |
|---|---|---|
| 1 | Network & Security Lead | `network/` |
| 2 | Zone A Cooling Controller | `zone-a/` |
| 3 | Zone B Controller & Failure Detection | `zone-b/` |
| 4 | Safety & Monitoring Lead | `safety-monitoring/` |

Each member edits only their own folder. Shared files (`README.md`, `docs/conventions.md`, `docs/test-results.md`) are edited by anyone, through a pull request.

## Architecture

- **Network:** 1 router (Core-RTR, 2911), 2 switches (Access-SW1, Access-SW2, 2960-24TT), router-on-a-stick, DHCP, 1 ACL.
- **VLANs:** 10 Servers, 20 IoT, 30 Management, plus 999 as an unused native VLAN.
- **Servers:** Srv-Web, Srv-DB, Srv-File (VLAN 10) and IoT-Server (VLAN 20).
- **Controllers:** three SBC-PT boards running Python: SBC-ZoneA, SBC-ZoneB, SBC-Monitor (VLAN 20).
- **Admin-PC** on VLAN 30 for monitoring and testing.

| VLAN | Name | Subnet | Gateway |
|---:|---|---|---|
| 10 | Servers | 192.168.10.0/24 | 192.168.10.1 |
| 20 | IoT | 192.168.20.0/24 | 192.168.20.1 |
| 30 | Management | 192.168.30.0/24 | 192.168.30.1 |

Fixed addresses: Srv-Web `.10.10`, Srv-DB `.10.11`, Srv-File `.10.12`, IoT-Server `.20.10`, SBC-ZoneA `.20.20`, SBC-ZoneB `.20.21`, SBC-Monitor `.20.22`, Admin-PC `.30.10`. DHCP serves from `.100` upward in each subnet. Full details are in `docs/conventions.md`.

## Folder guide

```
data-center-monitoring/
├── README.md                    # Project overview, team, how to run
├── docs/
│   ├── HANDOFF.md               # Status + next steps for each member
│   ├── conventions.md           # Device names, VLAN/IP table, thresholds
│   └── test-results.md          # Test table T1-T17 with screenshots
├── network/                     # Member 1
│   ├── network_config.txt       # All IOS commands
│   ├── ip-vlan-tables.md        # IP/VLAN tables
│   ├── topology.png             # Topology diagram
│   ├── datacenter_master.pkt    # Master Packet Tracer file (Member 1 only)
│   └── screenshots/             # ACL, DHCP, port-security evidence
├── zone-a/                      # Member 2
│   ├── zoneA_controller.py      # SBC-ZoneA script
│   ├── zoneA_flowchart.png      # Logic flowchart
│   ├── pin-map.md               # Sensor and cooler pins
│   └── screenshots/             # Hysteresis test evidence
├── zone-b/                      # Member 3
│   ├── zoneB_controller.py      # SBC-ZoneB script + failure detection
│   ├── pin-map.md               # Sensor, cooler, siren pins
│   └── screenshots/             # Failure scenario evidence
├── safety-monitoring/           # Member 4
│   ├── monitor.py               # SBC-Monitor script
│   ├── iot-rules.md             # IoT server rules table
│   ├── pin-map.md               # Sensor and actuator pins
│   └── screenshots/             # Dashboard and safety evidence
└── report/
    └── final-report.pdf         # Final report for submission
```

## How to run

1. Open `network/master/datacenter_master.pkt` in Cisco Packet Tracer (the project was built in version 9.0).
2. Double-click an SBC, open the **Programming** tab, click `main.py`, and paste the matching script (`zoneA_controller.py`, `zoneB_controller.py`, `monitor.py`).
3. Click **Run**. The output appears in the console at the bottom of the same tab.
4. Each controller has a `TEST_MODE` setting near the top: `True` runs a built-in test sequence, `False` reads the real sensors.

## Shared thresholds

| Parameter | Value |
|---|---|
| CRAC ON | >= 27 °C |
| CRAC OFF | <= 22 °C |
| Critical | >= 35 °C |
| Humidity fan ON / OFF | > 60 % / < 50 % |

Between 22 and 27 °C the controller holds its previous state (hysteresis).

## Working rules

- One owner per folder. Work on your own branch (`member1-network`, `member2-zone-a`, `member3-zone-b`, `member4-monitoring`) and merge through a pull request.
- **Only Member 1 edits `network/master/datacenter_master.pkt`.** A `.pkt` is a binary file that Git cannot merge. Everyone else builds in their own file under `pkt-parts/` and sends it to Member 1 to paste into the master.
- Use the agreed device names exactly: Core-RTR, Access-SW1, Access-SW2, Srv-Web, Srv-DB, Srv-File, IoT-Server, SBC-ZoneA, SBC-ZoneB, SBC-Monitor, RackA-Temp, RackB-Temp, CRAC-A, CRAC-B, Admin-PC.
- Each actuator is controlled by exactly one controller (script or IoT rule), never both.
- Record real results only. Every test needs steps, expected result, actual result, pass/fail and a screenshot.

## Status

See `docs/HANDOFF.md` for what is done, what is open, and what each member does next. Test results are tracked in `docs/test-results.md`.
