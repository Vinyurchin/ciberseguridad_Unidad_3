from flask import Flask, render_template
from flask_socketio import SocketIO
from scapy.all import sniff, IP, TCP, UDP, ICMP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def mostrar_paquete(paquete):
    if IP in paquete:
        # Extraer información del paquete
        datos = {
            "origen": paquete[IP].src,
            "destino": paquete[IP].dst,
            "protocolo": paquete[IP].proto,
            "puerto_origen": None,
            "puerto_destino": None,
        }

        # Verificar si es TCP o UDP para agregar puertos
        if TCP in paquete:
            datos["puerto_origen"] = paquete[TCP].sport
            datos["puerto_destino"] = paquete[TCP].dport
        elif UDP in paquete:
            datos["puerto_origen"] = paquete[UDP].sport
            datos["puerto_destino"] = paquete[UDP].dport
        elif ICMP in paquete:
            datos["protocolo"] = "ICMP"

        # Enviar los datos a la página web en tiempo real
        socketio.emit('nuevo_paquete', datos)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('iniciar_sniffer')
def iniciar_sniffer():
    # Iniciar el sniffer en un hilo separado
    sniff(prn=mostrar_paquete, filter="ip", store=0)

if __name__ == '__main__':
    socketio.run(app, debug=True)