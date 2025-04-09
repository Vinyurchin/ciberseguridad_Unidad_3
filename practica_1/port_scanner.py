from flask import Flask, request, render_template
import nmap

app = Flask(__name__)

def scan_ports(target_ip, ports):
    nm = nmap.PortScanner()
    results = []

    nm.scan(hosts=target_ip, arguments=f'-p {ports}')

    if nm.all_hosts():
        for host in nm.all_hosts():
            if 'tcp' in nm[host]:
                for port in nm[host]['tcp']:
                    state = nm[host]['tcp'][port]['state']
                    if state == "open":
                        results.append(f"Puerto {port}: {state}")
                    elif ports.isdigit():
                        results.append(f"Puerto {port}: {state}")
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form['target']
    option = request.form['option']
    ports = ""

    if option == "1": 
        ports = request.form['port']
    elif option == "2":
        ports = request.form['port_range']
    elif option == "3":
        ports = "1-65535"

    results = scan_ports(target, ports)

    if option == "1" and len(results) == 0:
        results.append(f"El puerto {ports} está cerrado.")
    elif len(results) == 0:
        results.append("No se encontraron puertos abiertos.")

    return render_template('results.html', target=target, results=results)

if __name__ == "__main__":
    app.run(debug=True)