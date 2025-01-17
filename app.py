import yaml,psutil,platform,requests

with open('./config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)
clientname = config['client']['clientname']
print(f"Start collecting status for {clientname} sosu!")

data = {}

print("==== System Info ====")
uname = platform.uname()
data['system'] = uname.system
print(f"System: {data['system']}")
data['machine'] = uname.machine
print(f"Machine: {data['machine']}")
data['processor'] = uname.processor
print(f"Processor: {data['processor']}")
print()

print("==== CPU Info ====")
data['cpu_usage'] = {}
data['cpu_usage']['physical_cores'] = psutil.cpu_count(logical=False)
data['cpu_usage']['total_cores'] = psutil.cpu_count(logical=True)
data['cpu_usage']['frequency'] = format(psutil.cpu_freq().current,".2f")
data['cpu_usage']['usage'] = psutil.cpu_count(logical=False)
print(f"Physical cores: {data['cpu_usage']['physical_cores']}")
print(f"Total cores: {data['cpu_usage']['total_cores']}")
print(f"Current Frequency: {data['cpu_usage']['frequency']} MHz")
print(f"Usage: {data['cpu_usage']['usage']} %")
print()

print("==== Memory Info ====")
svmem = psutil.virtual_memory()
data['mem_usage'] = {}
data['mem_usage']['total'] = format(svmem.total / (1024 ** 3),".2f")
data['mem_usage']['available'] = format(svmem.available / (1024 ** 3),".2f")
data['mem_usage']['used'] = format(svmem.used / (1024 ** 3),".2f")
data['mem_usage']['usage'] = svmem.percent
print(f"Total: {data['mem_usage']['total']} GB")
print(f"Available: {data['mem_usage']['available']} GB")
print(f"Used: {data['mem_usage']['used']} GB")
print(f"Percentage: {data['mem_usage']['usage']}%")
print()

print("==== Disk Info ====")
partitions = psutil.disk_partitions()
data['disk'] = []
print("Device\tMountpoint\tFile Sys\tTotal\tFree\tUsed")
for partition in partitions:
    perpart = {}
    perpart['device'] = partition.device
    perpart['mountpoint'] = partition.mountpoint
    perpart['fs'] = partition.fstype
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    perpart['total'] = format(partition_usage.total / (1024 ** 3),".2f")
    perpart['used'] = format(partition_usage.used / (1024 ** 3),".2f")
    perpart['free'] = format(partition_usage.free / (1024 ** 3),".2f")
    perpart['usage'] = partition_usage.percent
    print(f"{perpart['device']}\t{perpart['mountpoint']}\t{perpart['fs']}\t{perpart['total']} GB\t{perpart['free']} GB\t{perpart['used']} GB ({perpart['usage']}%)")
    data['disk'].append(perpart)
print()

net_io = psutil.net_io_counters()
data['network'] = {}
data['network']['sent'] = net_io.bytes_sent
data['network']['received'] = net_io.bytes_recv
print(f"Total Bytes Sent: {data['network']['sent']}")
print(f"Total Bytes Received: {data['network']['received']}")
print()

hostAdd = config['host']['address']
hostSec = config['host']['secret']
postData = {}
postData['clientname'] = clientname
postData['secret'] = hostSec
postData['data'] = data
print(f"Now uploading result to host {hostAdd} sosu!")
response = requests.post(f"{hostAdd}/sync", json=postData)
if response.status_code == 200:
    print(f"Upload succeeded sosu!")
    print(f"Remote response: {response.text}")
else:
    print(f"Failed to upload with response code {response.status_code}.")
    print(f"Remote response: {response.text}")