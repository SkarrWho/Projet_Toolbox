import os
import subprocess
import xml.etree.ElementTree as ET
import pandas as pd
import sys

def scan_network(target):
    results_dir = "csv_results"
    os.makedirs(results_dir, exist_ok=True)

    xml_path = os.path.join(results_dir, "nmap_scan.xml")
    csv_path = os.path.join(results_dir, "scan_results.csv")

    print(f"[*] Scanning {target} with Nmap...")

    nmap_command = [
        "nmap", "-sS", "-sV", "--version-intensity", "5", "--max-retries", "2",
        "--host-timeout", "2m", "-T4", "-Pn", "-O", "-oX", xml_path, target
    ]
    subprocess.run(nmap_command)

    print("[*] Scan complete. Parsing results...")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    hosts = []
    for host in root.findall("host"):
        ip_elem = host.find("address")
        ip = ip_elem.get("addr") if ip_elem is not None else None

        # 🧠 OS detection améliorée
        os_name = "Unknown"
        os_elem = host.find("os")
        if os_elem is not None:
            os_match = os_elem.find("osmatch")
            if os_match is not None and os_match.get("name"):
                os_name = os_match.get("name")
        if os_name == "Unknown":
            hostscript = host.find("hostscript")
            if hostscript is not None:
                for script in hostscript.findall("script"):
                    if "os" in script.get("id", "").lower():
                        os_name = script.get("output", "Unknown")

        for port in host.findall(".//port"):
            port_id = port.get("portid")
            state = port.find("state").get("state")
            service = port.find("service").get("name") if port.find("service") is not None else "Unknown"
            version = port.find("service").get("version") if port.find("service") is not None else "Unknown"

            if state == "open":
                hosts.append({
                    "ip": ip,
                    "port": port_id,
                    "service": service,
                    "version": version,
                    "os": os_name
                })

    df = pd.DataFrame(hosts)
    df.to_csv(csv_path, index=False)
    print(f"[+] Scan results saved to {csv_path}")
    return df

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <target_ip_or_range>")
        sys.exit(1)

    target_input = sys.argv[1]
    scan_network(target_input)
#[Jun 16, 2025 - 14:31:19 (EDT)] exeg
