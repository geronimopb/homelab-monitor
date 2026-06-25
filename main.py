from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import psutil
import docker
import datetime

app = FastAPI(title="Homelab Monitor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_docker_client():
    try:
        return docker.from_env()
    except:
        return None

@app.get("/api/system")
def system_info():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    uptime_seconds = datetime.datetime.now().timestamp() - psutil.boot_time()
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))

    return {
        "cpu_percent": cpu,
        "ram_total_gb": round(ram.total / 1e9, 2),
        "ram_used_gb": round(ram.used / 1e9, 2),
        "ram_percent": ram.percent,
        "disk_total_gb": round(disk.total / 1e9, 2),
        "disk_used_gb": round(disk.used / 1e9, 2),
        "disk_percent": disk.percent,
        "uptime": uptime,
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/api/containers")
def containers():
    client = get_docker_client()
    if not client:
        return {"error": "Docker no disponible", "containers": []}
    
    result = []
    for c in client.containers.list(all=True):
        result.append({
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
        })
    return {"containers": sorted(result, key=lambda x: x["name"])}

@app.get("/api/disks")
def disks():
    partitions = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                "mountpoint": part.mountpoint,
                "device": part.device,
                "total_gb": round(usage.total / 1e9, 2),
                "used_gb": round(usage.used / 1e9, 2),
                "percent": usage.percent
            })
        except:
            pass
    return {"disks": partitions}

@app.get("/api/health")
def health():

    return {"status": "ok"}
app.mount("/", StaticFiles(directory="static", html=True), name="static")
