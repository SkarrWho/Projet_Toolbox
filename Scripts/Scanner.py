import subprocess

def scan_target(target):
    print(f"[+] Scan de {target} (top 1000 ports + versions)...")
    result = subprocess.run(
        ["nmap", "-Pn", "-sV", "--top-ports", "1000", target],
        capture_output=True, text=True
    )
    return result.stdout