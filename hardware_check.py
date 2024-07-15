import psutil
import logging
import GPUtil
from pySMART import DeviceList

# Setup logging
logging.basicConfig(filename='hardware_monitoring.log', level=logging.INFO, format='%(asctime)s: %(message)s')

def log_message(message):
    print(message)
    logging.info(message)

def check_cpu_usage():
    try:
        for i, percentage in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
            message = f"CPU Core {i}: Usage {percentage}%"
            log_message(message)
            if percentage > 80:
                log_message(f"Warning: High CPU Usage on Core {i}")
    except Exception as e:
        log_message(f"Error checking CPU usage: {e}")

def check_memory_usage():
    try:
        memory = psutil.virtual_memory()
        message = f"Memory Usage: {memory.percent}%"
        log_message(message)
        if memory.percent > 80:
            log_message("Warning: High Memory Usage")
    except Exception as e:
        log_message(f"Error checking memory usage: {e}")

def check_disk_usage():
    try:
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            message = f"Disk {partition.device}: {usage.percent}% used"
            log_message(message)
            if usage.percent > 90:
                log_message(f"Warning: High Disk Usage on {partition.device}")
    except Exception as e:
        log_message(f"Error checking disk usage: {e}")

def check_gpu_usage():
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            message = f"GPU: {gpu.name}, Load: {gpu.load*100}%, Temperature: {gpu.temperature} C"
            log_message(message)
    except Exception as e:
        log_message(f"Error checking GPU usage: {e}")

def check_hard_drive_health():
    try:
        devices = DeviceList()
        for device in devices:
            if device is not None and device.assessment == 'FAIL':
                log_message(f"Warning: Hard Drive {device.name} ({device.model}) may be failing.")
    except Exception as e:
        log_message(f"Error checking hard drive health: {e}")

# Modify this section to call the new functions
def run_health_checks():
    check_cpu_usage()
    check_memory_usage()
    check_disk_usage()
    check_gpu_usage()
    check_hard_drive_health()

run_health_checks()