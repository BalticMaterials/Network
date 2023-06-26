#!/usr/bin/python3
############################################################################################
#
#   Name:       systemstats.py
#   Date:       24.06.2023
#   Version:    0.9
#   Source:     https://www.thepythoncode.com/article/get-hardware-system-information-python
#   Info:       Get data from system to store it in JSON file. 2 Files are created.
#   Input:      System data
#   Output:     JSON file -> dictionary-gpu.json & dictonary_system.json
#   Author:     Tjark Ziehm
#   
############################################################################################

import json
import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
        
print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")

# Boot Time
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

##################################---CPU USAGE--- #################################
# let's print CPU information
print("="*40, "CPU Info", "="*40)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

##################################---Memory USAGE--- #################################
# Memory Information
print("="*40, "Memory Information", "="*40)
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")

##################################---DISK USAGE--- #################################
# Disk Information
print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")

##################################---NETWORK INFO--- #################################
# Network information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

##################################---CREATE System-JSON---#################################
# Data to be written
cpu_percent = psutil.cpu_percent()
cpu_system = uname.system
node_name = uname.node
now = datetime.now()

dictionary_system = {
    "System":                   "{}".format(cpu_system),
    "Messurment Time":          "{}".format(now),
    "Node Name":                "{}".format(node_name),
    "Boot Time":                "{}".format(bt),
    "CPU: Current Frequency":   "{}".format(cpu_percent) ,
    "CPU: Usage Per Core: ":    "{}".format(cpu_percent),
    "CPU: Total CPU Usage":     f"{psutil.cpu_percent()}",
    "Memory: Used":             f"{get_size(svmem.used)}",
    "Memory: Percentage ":      f"{svmem.percent}%",
    "Disk Used ":               f"{get_size(partition_usage.used)}",
    "Disk Free ":               f"{get_size(partition_usage.free)}",
    "Disk Percentage ":         f"{partition_usage.percent}%",
    "Network Information":      if_addrs   
}

############################---GPU INFORMATION---##############################################
# GPU information
import GPUtil
from tabulate import tabulate

print("="*40, "GPU Details", "="*40)
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPU
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))
    ##################################---CREATE GPU-DICTONARY---#################################    
    dictionary_gpu = {
    "gpu_id": gpu_id,
    "gpu_name": gpu_name,
    "gpu_load": gpu_load,
    "gpu_free_memory": gpu_free_memory,
    "gpu_used_memory": gpu_used_memory,
    "gpu_total_memory": gpu_total_memory,
    "gpu_temperature": gpu_temperature,
    "gpu_uuid": gpu_uuid,
}

print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                   "temperature", "uuid")))

#####################################---Write-JSON---#################################### 
# Serializing json
json_object = json.dumps(dictionary_system, indent=13)
 
# Writing to sample.json
with open("dictionary_system.json", "w") as outfile:
    outfile.write(json_object)
    
# Serializing json
json_object = json.dumps(dictionary_gpu, indent=8)
 
# Writing to sample.json
with open("dictionary_gpu.json", "w") as outfile:
    outfile.write(json_object)