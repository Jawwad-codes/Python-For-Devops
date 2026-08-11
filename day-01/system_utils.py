# create a function that can  be reused , it should show the system info
import psutil
def system_info():
    cpu=psutil.cpu_percent(interval=1)
    ram=psutil.virtual_memory().percent
    disk=psutil.disk_usage("/").percent

    info={
        "cpu": cpu,
        "ram": ram,
        "memory": disk
    }

    return info