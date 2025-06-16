from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import threading
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

scan_lock = threading.Lock()

# Dictionnaire des modules et leurs scripts associés
module_scripts = {
    "ToolBox": "../ToolBox.py",
    "scanner": "../scanner.py",
    "vuln_finder": "../vuln_finder.py",
    "eternalblue": "../every_exploits/eternalblue.py",
    "ms08_067": "../every_exploits/MS08-067.py",
    "shellshock": "../every_exploits/Shellshock.py",
    "heartbleed": "../every_exploits/Heartbleed.py",
    "drupalgeddon": "../every_exploits/Drupalgeddon.py"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target_ip = request.form["target"]
    selected_module = request.form["module"]

    if scan_lock.locked():
        flash("Un scan est déjà en cours. Veuillez patienter.", "danger")
        return redirect(url_for("index"))

    script_path = module_scripts.get(selected_module)

    if not script_path or not os.path.exists(script_path):
        flash("❌ Le module demandé est introuvable ou mal nommé.", "danger")
        return redirect(url_for("index"))

    def run_script(ip, path):
        with scan_lock:
            try:
                if selected_module in ["ToolBox", "scanner"]:
                    subprocess.run(["python3", path, ip])
                else:
                    subprocess.run(["python3", path])
            except Exception as e:
                print(f"[!] Erreur pendant l'exécution : {e}")

    threading.Thread(target=run_script, args=(target_ip, script_path), daemon=True).start()
    flash(f"✅ Module '{selected_module}' lancé pour {target_ip}.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
