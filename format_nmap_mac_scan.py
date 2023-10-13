import sys

hosts = []
curr_host_idx = None

for line in sys.stdin:
    # IP (and hostname)
    if "nmap scan report" in line.lower():
        hosts.append({
            "host": line.lower().split("nmap scan report for ")[-1].strip(),
            "mac": None,
            "manufacturer": None,
            "is_host_up": None
        })
        curr_host_idx = 0 if curr_host_idx is None else (curr_host_idx + 1)
    # latency
    if "host is up" in line.lower():
        hosts[curr_host_idx]["is_host_up"] = line.strip()
    # MAC & manufacturer name
    if "mac address" in line.lower():
        _mac, _manufacturer = line.lower().split("mac address: ")[-1].strip().split(' ')
        hosts[curr_host_idx]["mac"] = _mac
        hosts[curr_host_idx]["manufacturer"] = _manufacturer.replace('(', '').replace(')', '')

# print to CLI
print("Host | MAC | Manufacturer | Is Host Up?")
for host in hosts:
    print("{0} | {1} | {2} | {3}".format(
            host["host"],
            host["mac"],
            host["manufacturer"],
            host["is_host_up"]
    ))

# e.g.
# sudo nmap -sn 192.168.0.1/24 | python3 format_nmap_mac_scan.py
