from flask import Flask, render_template, request, jsonify
import subprocess
import json
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Render the main home page with tool selection."""
    return render_template('accueil.html')

@app.route('/nmap-scan')
def nmap_scan():
    """Render the Nmap scan form page."""
    return render_template('index.html')

@app.route('/resultats')
def resultats():
    """Render the results page that will display scan results."""
    target_ip = request.args.get('ip', '').strip()
    target_domain = request.args.get('domain', '').strip()
    scan_type = request.args.get('type')
    ports = request.args.get('ports')
    
    # Determine target display
    if target_ip and target_domain:
        target = f"{target_ip} ({target_domain})"
    elif target_ip:
        target = target_ip
    elif target_domain:
        target = target_domain
    else:
        target = "Cible inconnue"
    
    return render_template('resultats.html', 
                           target=target,
                           scan_type=scan_type,
                           ports=ports)

@app.route('/scan', methods=['POST'])
def scan():
    """Handle scan requests and return Nmap results as JSON."""
    data = request.json
    target = data.get('target')
    scan_type = data.get('scan_type')
    ports = data.get('ports')
    
    if not target:
        return jsonify({'error': 'No target specified'}), 400
    
    try:
        # Build nmap command
        cmd = ['nmap', '-oX', '-']
        
        if scan_type == 'top':
            # Scan top 1000 ports
            cmd.extend(['-sV', '--top-ports', '1000'])
        else:
            # Scan custom ports
            if not ports:
                return jsonify({'error': 'No ports specified for custom scan'}), 400
            cmd.extend(['-sV', '-p', ports])
        
        # Add target
        cmd.append(target)
        
        logging.debug(f"Running command: {' '.join(cmd)}")
        
        # Run nmap
        process = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if process.returncode != 0:
            logging.error(f"Nmap error: {process.stderr}")
            return jsonify({'error': f'Nmap scan failed: {process.stderr}'}), 500
        
        # Parse XML output from nmap
        xml_output = process.stdout
        
        # Extract results using regex (basic parsing)
        result = parse_nmap_xml(xml_output, target)
        
        if not result:
            return jsonify({'error': 'Failed to parse scan results or no hosts found'}), 404
        
        return jsonify({'results': result})
    except Exception as e:
        logging.error(f"Scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def parse_nmap_xml(xml_output, target):
    """Parse Nmap XML output using regex."""
    result = []
    
    # Find all hosts
    host_blocks = re.findall(r'<host[^>]*>.*?</host>', xml_output, re.DOTALL)
    
    for host_block in host_blocks:
        # Get host address
        address_match = re.search(r'<address addr="([^"]*)"', host_block)
        if not address_match:
            continue
        
        host_address = address_match.group(1)
        
        # Get host state
        state_match = re.search(r'<status state="([^"]*)"', host_block)
        host_state = state_match.group(1) if state_match else 'unknown'
        
        # Get hostname if available
        hostname_match = re.search(r'<hostname name="([^"]*)"', host_block)
        hostname = hostname_match.group(1) if hostname_match else ''
        
        host_result = {
            'host': host_address,
            'hostname': hostname,
            'state': host_state,
            'ports': []
        }
        
        # Find all ports
        port_blocks = re.findall(r'<port [^>]*>.*?</port>', host_block, re.DOTALL)
        
        for port_block in port_blocks:
            # Get port number
            port_match = re.search(r'portid="(\d+)"', port_block)
            if not port_match:
                continue
            
            port_number = int(port_match.group(1))
            
            # Get port state
            state_match = re.search(r'<state state="([^"]*)"', port_block)
            port_state = state_match.group(1) if state_match else 'unknown'
            
            # Get service name
            service_match = re.search(r'<service name="([^"]*)"', port_block)
            service_name = service_match.group(1) if service_match else ''
            
            # Get product and version if available
            product_match = re.search(r'product="([^"]*)"', port_block)
            version_match = re.search(r'version="([^"]*)"', port_block)
            
            product = product_match.group(1) if product_match else ''
            version = version_match.group(1) if version_match else ''
            
            host_result['ports'].append({
                'port': port_number,
                'state': port_state,
                'service': service_name,
                'version': f"{product} {version}".strip()
            })
        
        result.append(host_result)
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
