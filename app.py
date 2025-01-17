import yaml,psutil,platform,requests,json,datetime

try:
    with open('./config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    clientname = config['client']['clientname']
    printstatus = config['client']['printstatus']
    log = config['client']['log']
    if printstatus is None:
        printstatus = True
    upload = config['client']['upload']
    if upload is None:
        upload = True
    if log is None:
        log = False

except:
    print("Cannot read config.yml. Collect status only.")
    printstatus = True

if clientname:
    print(f"Start collecting status for {clientname} sosu!")
else:
    print("No clientname specified. Collect status only.")
    upload = False

data = {}

uname = platform.uname()
data['system'] = uname.system
data['machine'] = uname.machine
data['processor'] = uname.processor
if printstatus:
    print("==== System Info ====")
    print(f"System: {data['system']}")
    print(f"Processor: {data['processor']}")
    print()

data['cpu_usage'] = {}
data['cpu_usage']['physical_cores'] = psutil.cpu_count(logical=False)
data['cpu_usage']['total_cores'] = psutil.cpu_count(logical=True)
data['cpu_usage']['frequency'] = format(psutil.cpu_freq().current,".2f")
data['cpu_usage']['usage'] = psutil.cpu_count(logical=False)
if printstatus:
    print("==== CPU Info ====")
    print(f"Physical cores: {data['cpu_usage']['physical_cores']}")
    print(f"Total cores: {data['cpu_usage']['total_cores']}")
    print(f"Current Frequency: {data['cpu_usage']['frequency']} MHz")
    print(f"Usage: {data['cpu_usage']['usage']} %")
    print()

svmem = psutil.virtual_memory()
data['mem_usage'] = {}
data['mem_usage']['total'] = format(svmem.total / (1024 ** 3),".2f")
data['mem_usage']['available'] = format(svmem.available / (1024 ** 3),".2f")
data['mem_usage']['used'] = format(svmem.used / (1024 ** 3),".2f")
data['mem_usage']['usage'] = svmem.percent
if printstatus:
    print("==== Memory Info ====")
    print(f"Total: {data['mem_usage']['total']} GB")
    print(f"Available: {data['mem_usage']['available']} GB")
    print(f"Used: {data['mem_usage']['used']} GB")
    print(f"Percentage: {data['mem_usage']['usage']}%")
    print()

if uname.system != "Windows":
    swap = psutil.swap_memory()
    data['swap_usage'] = {}
    data['swap_usage']['total'] = format(swap.total / (1024 ** 3),".2f")
    data['swap_usage']['free'] = format(swap.free / (1024 ** 3),".2f")
    data['swap_usage']['used'] = format(swap.used / (1024 ** 3),".2f")
    data['swap_usage']['usage'] = swap.percent
    if printstatus:
        print("==== Swap Info ====")
        print(f"Total: {data['swap_usage']['total']} GB")
        print(f"Free: {data['swap_usage']['free']} GB")
        print(f"Used: {data['swap_usage']['used']} GB")
        print(f"Percentage: {data['swap_usage']['usage']}%")
        print()

partitions = psutil.disk_partitions()
spec = config['client']['spec-disks']['enable']
if spec is None:
    spec = False
data['disk'] = []
if printstatus:
    print("==== Disk Info ====")
    print("Device\tMountpoint\tFile Sys\tTotal\tFree\tUsed")
for partition in partitions:
    perpart = {}
    perpart['device'] = partition.device
    perpart['mountpoint'] = partition.mountpoint
    perpart['fs'] = partition.fstype
    if (spec and perpart['mountpoint'] in config['client']['spec-disks']['mountpoints']) or (not spec):
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        perpart['total'] = format(partition_usage.total / (1024 ** 3),".2f")
        perpart['used'] = format(partition_usage.used / (1024 ** 3),".2f")
        perpart['free'] = format(partition_usage.free / (1024 ** 3),".2f")
        perpart['usage'] = partition_usage.percent
        if printstatus:
            print(f"{perpart['device']}\t{perpart['mountpoint']}\t{perpart['fs']}\t{perpart['total']} GB\t{perpart['free']} GB\t{perpart['used']} GB ({perpart['usage']}%)")
        data['disk'].append(perpart)
    else:
        continue
if printstatus:
    print()

net_io = psutil.net_io_counters()
data['network'] = {}
data['network']['sent'] = net_io.bytes_sent
data['network']['received'] = net_io.bytes_recv
if printstatus:
    print(f"Total Bytes Sent: {data['network']['sent']}")
    print(f"Total Bytes Received: {data['network']['received']}")
    print()

hostAdd = config['host']['address']
hostSec = config['host']['secret']
postData = {}
postData['clientname'] = clientname
postData['secret'] = hostSec
postData['data'] = data
current_time = datetime.datetime.now()
if log:
    logName = current_time.strftime("%Y%m%d%H%M%S")
    print(f"Writing log file to logs/{logName}.json, please wait.")
    try:
        with open(f'logs/{logName}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        print("Log succeeded sosu!")
    except:
        print("Fail to write log file!")
print()
if upload:
    print(f"Now uploading result to host {hostAdd} sosu!")
    try:
        response = requests.post(f"{hostAdd}/sync", json=postData)
        if response.status_code == 200:
            print(f"Upload succeeded sosu!")
            print(f"Remote response: {response.text}")
        else:
            print(f"Failed to upload with response code {response.status_code}.")
            print(f"Remote response: {response.text}")
    except:
        print("There was a problem when initiating the request sosu!")
print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} Collection completed sosu.")