import os
import glob
import re
import platform
import subprocess
import psutil

try:
    import GPUtil
except ImportError:
    GPUtil = None

def get_hardware_power_usage():
    try:
        # Check laptop battery
        for battery_dir in glob.glob("/sys/class/power_supply/BAT*"):
            power_now_file = os.path.join(battery_dir, "power_now")
            current_now_file = os.path.join(battery_dir, "current_now")
            voltage_now_file = os.path.join(battery_dir, "voltage_now")
            status_file = os.path.join(battery_dir, "status")
            
            status = "Discharging"
            if os.path.exists(status_file):
                with open(status_file, "r") as f:
                    status = f.read().strip()
            
            if status == "Discharging":
                if os.path.exists(power_now_file):
                    with open(power_now_file, "r") as f:
                        val = float(f.read().strip())
                        if val > 0:
                            return val / 1_000_000.0 # microwatts to Watts
                elif os.path.exists(current_now_file) and os.path.exists(voltage_now_file):
                    with open(current_now_file, "r") as f_c, open(voltage_now_file, "r") as f_v:
                        curr = float(f_c.read().strip())
                        volt = float(f_v.read().strip())
                        return (curr * volt) / 1_000_000_000_000.0
    except Exception:
        pass
    return None

def get_cpu_model():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or "Unknown CPU"

def get_os_version():
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                info = {}
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        info[k] = v.strip('"')
                return info.get("PRETTY_NAME", platform.platform())
    except Exception:
        pass
    return platform.platform()

def get_gpu_info():
    gpus = []
    # 1. Try lspci for system GPUs
    try:
        res = subprocess.check_output("lspci -nn", shell=True).decode("utf-8")
        for line in res.split("\n"):
            if "vga" in line.lower() or "3d" in line.lower() or "display" in line.lower():
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    gpu_name = parts[2].strip()
                    gpu_name = re.sub(r'\(rev \d+\)', '', gpu_name).strip()
                    gpus.append(gpu_name)
    except Exception:
        pass

    # 2. Try nvidia-smi
    try:
        nvidia_res = subprocess.check_output(
            "nvidia-smi --query-gpu=name,driver_version,memory.total,temperature.gpu,utilization.gpu --format=csv,noheader,nounits",
            shell=True
        ).decode("utf-8")
        nvidia_gpus = []
        for line in nvidia_res.strip().split("\n"):
            if line.strip():
                fields = [f.strip() for f in line.split(",")]
                if len(fields) >= 5:
                    name, driver, mem_total, temp, util = fields
                    nvidia_gpus.append({
                        "name": f"NVIDIA {name}",
                        "driver": driver,
                        "mem_total": f"{mem_total} MB",
                        "temp": f"{temp}°C",
                        "usage": f"{util}%"
                    })
        if nvidia_gpus:
            return nvidia_gpus
    except Exception:
        pass

    if gpus:
        return [{"name": name, "driver": "System Driver", "mem_total": "Dynamic Shared", "temp": "N/A", "usage": "N/A"} for name in gpus]
    
    return [{"name": "Standard Graphics Controller", "driver": "N/A", "mem_total": "N/A", "temp": "N/A", "usage": "N/A"}]
