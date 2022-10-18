from prometheus_client import start_http_server, Gauge, Info
import time
import subprocess
import prometheus_client
import json


# Disabling default Collector metrics
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


# Сonstants definitions
TIME_SLEEP = 2
SERVER_PORT = 9090              # port to expose metrics


# Labels & constant values definitions
hostname = subprocess.check_output(
    ["cat", "/etc/hostname"]).decode("utf-8").rstrip()
ipinfo_out = json.loads(subprocess.check_output(
    ["wget", "-qO-", "ipinfo.io"]).decode("utf-8"))
ip_address = ipinfo_out["ip"]
country = ipinfo_out["country"]
city = ipinfo_out["city"]
location = ipinfo_out["loc"]
cores = subprocess.check_output(["nproc"]).decode("utf-8").rstrip()
mem_total = subprocess.check_output(["free"]).decode("utf-8").split()[7]
disk_total = int(subprocess.check_output(
    ["df", "/"]).decode("utf-8").split()[8]) * 1024


# Metrics definitions
#################################################################################
#
METRICS_LABELS = [hostname, ip_address]
#
LABELS = ['host', 'ip']
#################################################################################
loadavg_1 = Gauge('loadavg_1', 'average load per 1s', LABELS)
loadavg_5 = Gauge('loadavg_5', 'average load per 5s', LABELS)
loadavg_15 = Gauge('loadavg_15', 'average load per 15s', LABELS)
mem_available = Gauge('mem_available', 'available memory on the host', LABELS)
disk_available = Gauge('disk_available', 'available space on the disk', LABELS)
host_uptime = Gauge('host_uptime', 'host uptime', LABELS)
host = Info('host', 'info', LABELS)


# Functions definitions
def loadavg():
    res = subprocess.check_output(["cat", "/proc/loadavg"])
    avg_1 = res.decode("utf-8").split()[0]
    avg_5 = res.decode("utf-8").split()[1]
    avg_15 = res.decode("utf-8").split()[2]
    loadavg_1.labels(*METRICS_LABELS).set(avg_1)
    loadavg_5.labels(*METRICS_LABELS).set(avg_5)
    loadavg_15.labels(*METRICS_LABELS).set(avg_15)


def loadmem():
    available = subprocess.check_output(["free"]).decode("utf-8").split()[12]
    mem_available.labels(*METRICS_LABELS).set(available)


def disk():
    disk_out = subprocess.check_output(["df", "/"]).decode("utf-8").split()
    available = int(disk_out[10]) * 1024
    disk_available.labels(*METRICS_LABELS).set(available)


def uptime_host():
    uptime = subprocess.check_output(
        ["cat", "/proc/uptime"]).decode("utf-8").split()[0]
    host_uptime.labels(*METRICS_LABELS).set(uptime)


# RUN expose metrics
start_http_server(SERVER_PORT)

# expose static metrics
host.labels(*METRICS_LABELS).info({'cpu_cores': cores, 'mem_total': mem_total,
                                   'disk_total': str(disk_total), 'country': country, 'city': city, 'location': location})

# expose dynamic metrics
while True:
    uptime_host()
    loadmem()
    disk()
    loadavg()

    time.sleep(TIME_SLEEP)
