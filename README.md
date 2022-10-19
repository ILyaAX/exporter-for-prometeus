# exporter-for-prometeus

Exporter to provide metrics for Prometeus.

The following dependencies must be established:
```
apt install python3-pip
pip install prometheus-client
```
Copying files to the host along the specified paths:
```
/usr/local/bin/exporter.py
/etc/systemd/system/exporter.service
```
Grant permissions to execute the exporter.py file:
```
sudo chmod +x /usr/local/bin/exporter.py
```
You can now manage the exporter service
```
systemctl {start/stop/enable/disable} exporter.service
```
