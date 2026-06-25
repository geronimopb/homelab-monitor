# Homelab Monitor

Real-time server monitoring dashboard running on a self-hosted Ubuntu Server 24.04 (CasaOS). Accessible from anywhere via Tailscale VPN.

Built with **FastAPI** and **Vanilla JS** — lightweight enough to run on modest hardware (2 cores, 4GB RAM) alongside other self-hosted services.

---

## Live Dashboard

![Dashboard preview](https://raw.githubusercontent.com/placeholder/homelab-monitor/main/docs/preview.png)

> Auto-refreshes every 15 seconds. Accessible via Tailscale from any device.

---

## Features

- **System metrics** — CPU usage, RAM consumption, disk usage with visual progress bars
- **Docker containers** — real-time status of all containers (running, exited, paused)
- **Storage overview** — all mounted partitions including MergerFS pool disks
- **Uptime tracking** — server uptime displayed in the header
- **Auto-refresh** — dashboard updates every 15 seconds automatically
- **Runs as systemd service** — starts automatically on boot, restarts on failure

---

## Architecture

```
Browser (any device on Tailscale)
         │
         │ HTTP via Tailscale VPN
         ▼
Ubuntu Server 24.04 (CasaOS)
├── homelab-monitor (this project)
│   ├── FastAPI — serves REST API + static frontend
│   ├── psutil  — reads CPU, RAM, disk metrics
│   └── docker  — reads container status
├── Immich
├── FileBrowser
└── MergerFS pool (4x 2TB disks)
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.12 + FastAPI |
| System metrics | psutil |
| Container info | docker-py |
| Frontend | Vanilla JS + HTML + CSS |
| Process manager | systemd |
| Remote access | Tailscale VPN |
| Server OS | Ubuntu Server 24.04 LTS |

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional, for container monitoring)
- Tailscale (optional, for remote access)

### Install

```bash
git clone https://github.com/geronimopb/homelab-monitor.git
cd homelab-monitor
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn psutil docker
```

### Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in your browser.

### Run as systemd service (auto-start on boot)

```bash
sudo cp homelab-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable homelab-monitor
sudo systemctl start homelab-monitor
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/system` | CPU, RAM, disk, uptime |
| `GET` | `/api/containers` | Docker container status |
| `GET` | `/api/disks` | All mounted partitions |
| `GET` | `/api/health` | Health check |

---

## Hardware

- **CPU:** 2 cores
- **RAM:** 4 GB
- **Storage:** 1x 234 GB SSD (OS) + 4x 2 TB HDD (MergerFS pool)
- **OS:** Ubuntu Server 24.04 LTS + CasaOS

---

## License

MIT
