import os
import pandas as pd
import subprocess

def find_exploits(input_file="csv_results/scan_results.csv", output_file="csv_results/vuln_results.csv"):
    if not os.path.exists(input_file):
        print(f"[!] File not found: {input_file}")
        return

    os.makedirs("csv_results", exist_ok=True)
    df = pd.read_csv(input_file)
    exploit_results = []

    for index, row in df.iterrows():
        service = str(row['service'])
        version = str(row['version'])
        port = int(row['port'])
        os_name = str(row['os'])
        ip = row['ip']

        query = f"{service} {version}".strip()
        exploit_text = ""

        if query:
            print(f"[*] Searching exploits for: {query}")
            try:
                result = subprocess.run(
                    ["searchsploit", query],
                    capture_output=True,
                    text=True
                )
                output = result.stdout.strip()
                exploits = output.split('\n')[4:]  # Skip header
                exploit_text = "\n".join(exploits) if exploits else "No results"
            except Exception as e:
                exploit_text = f"Error running searchsploit: {e}"
        else:
            exploit_text = "No service/version info"

        # 🔥 Détection manuelle MS17-010
        if port == 445 and "Windows" in os_name:
            exploit_text += "\n[+] Possible MS17-010 (EternalBlue) vulnerability"

        exploit_results.append({
            "ip": ip,
            "port": port,
            "service": service,
            "version": version,
            "os": os_name,
            "exploits": exploit_text
        })

    result_df = pd.DataFrame(exploit_results)
    result_df.to_csv(output_file, index=False)
    print(f"[+] Vulnerability results saved to {output_file}")
    return result_df

if __name__ == "__main__":
    find_exploits()
