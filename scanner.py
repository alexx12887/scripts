import subprocess

# Run `arp -a` command and extract IP addresses
arp_output = subprocess.check_output(["arp", "-a"]).decode()
ips = [line.split("(")[1].split(")")[0] for line in arp_output.splitlines() if "ifscope permanent" not in line]

# Scan for open ports using nmap
for ip in ips:
    print("")
    print(f"Scanning {ip}...")
    try:
        nmap_output = subprocess.check_output(["nmap", "-F", ip]).decode()
    except subprocess.CalledProcessError as e:
        print(f"Error while scanning {ip}: {e}")
        continue

    # Extract open ports and their services from nmap output
    open_ports = []
    for line in nmap_output.splitlines():
        if "open" in line:
            port = line.split()[0]
            service = line.split()[2]
            open_ports.append((port, service))

    # Print results
    if open_ports:
        print("Open ports:")
        for port, service in open_ports:
            print(f"Port {port}: {service}")
    else:
        print("No open ports found.")
