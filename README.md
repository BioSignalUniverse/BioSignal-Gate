# BioSignal Gate

BioSignal Gate is a modular, device-agnostic bio-signal processing and decision framework.

It is designed around a clean architecture:

Measure → Process → Decide → Execute

The system supports:
- Real wearable integration (e.g., Polar H10)
- Simulation mode (no hardware required)
- Config-driven thresholds
- Weighted decision logic
- Structured API access
- Optional dashboard interface

---

## 🔹 Architecture

- `core/` → Decision logic, engine, and execution layer
- `sensors/` → Device adapters (Polar, simulation, future wearables)
- `config/` → Thresholds and system parameters
- `api.py` → Flask interface
- `templates/` → Dashboard interface

The engine is hardware-independent.
Sensors are pluggable.
Logic is fully config-driven.

---

## 🔹 Features

- Real-time HRV processing (RMSSD)
- Automatic device fallback to simulation
- Decision scoring system
- Logging support
- Health endpoint
- Optional dashboard view
- MIT licensed

---

## 🔹 Run Locally

```bash
pip install -r requirements.txt
python api.py
```

Open:

```
http://localhost:5000/dashboard
```

---

## 🔹 Philosophy

BioSignal Gate is built for:

- Open research
- Responsible signal interpretation
- Extensible system design
- Future wearable integration
- Transparent decision logic

It is not medical software.
It is a modular bio-signal framework.

---

## 🔹 License

MIT License