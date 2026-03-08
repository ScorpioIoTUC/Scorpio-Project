#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import time
from datetime import datetime
from gnuradio import gr
from gnuradio import soapy
import gnuradio.lora_sdr as lora_sdr

class MyLoraRx(gr.top_block):
    def __init__(self, 
                 samp_rate=1000000, 
                 center_freq=915000000, 
                 bw=250000, 
                 sf=7, 
                 cr=1, 
                 gain=20,
                 callback=None):
        """
        Clase para recibir mensajes LoRa usando RTL-SDR.
        :param callback: Función que se ejecuta al recibir un mensaje. 
                         Debe aceptar un argumento (el payload).
        """
        gr.top_block.__init__(self, "My LoRa Receiver")
        
        # Parámetros de configuración
        self.samp_rate = samp_rate
        self.center_freq = center_freq
        self.bw = bw
        self.sf = sf
        self.gain = gain
        self.callback = callback

        # 1. Fuente: RTL-SDR vía Soapy
        dev = 'driver=rtlsdr'
        stream_args = 'bufflen=16384'
        self.src = soapy.source(dev, "fc32", 1, '', stream_args, [''], [''])
        self.src.set_sample_rate(0, self.samp_rate)
        self.src.set_frequency(0, self.center_freq)
        self.src.set_gain_mode(0, False)
        self.src.set_gain(0, self.gain)

        # 2. Decodificador LoRa
        # print_rx=[False, True] permite que el bloque lora_rx imprima en consola
        self.lora_rx = lora_sdr.lora_sdr_lora_rx(
            bw=self.bw,
            cr=cr,
            has_crc=True,
            impl_head=False,
            pay_len=64,
            samp_rate=self.samp_rate,
            sf=self.sf,
            sync_word=[0x12],
            soft_decoding=True,
            ldro_mode=2,
            print_rx=[False, True] 
        )

        # 3. Sumidero de Mensajes (Message Sink)
        # Usamos un bloque "Message Debug" para capturar los mensajes PDU
        self.msg_sink = blocks.message_debug()

        # Conexiones de flujo (Streaming)
        self.connect((self.src, 0), (self.lora_rx, 0))

        # Conexión de Mensajes (Asíncrona)
        # Conectamos la salida 'out' de lora_rx al sistema de logs si quieres procesarlo
        self.msg_connect((self.lora_rx, 'out'), (self.msg_debug, 'store'))

    def start_rx(self):
        """Inicia el flujo de radio."""
        self.start()
        print(f"[*] Receptor iniciado en {self.center_freq/1e6} MHz...")

    def stop_rx(self):
        """Detiene el receptor de forma segura."""
        self.stop()
        self.wait()
        print("\n[*] Receptor detenido.")
        
def save_to_file(payload):
    """Función para procesar el mensaje recibido."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # El payload de lora_sdr suele venir como un vector de bytes
    try:
        # Intentamos decodificar como texto, si falla guardamos el hex
        data_str = "".join(chr(x) for x in payload if 31 < x < 127)
    except:
        data_str = str(payload)

    log_entry = f"[{timestamp}] - {data_str}\n"
    
    with open("lora_messages.txt", "a") as f:
        f.write(log_entry)
    
    print(f"--- Mensaje Guardado: {data_str}")

if __name__ == '__main__':
    # Configuración personalizada
    rx_node = MyLoraRx(
        center_freq=915e6, # 915 MHz
        sf=7,
        bw=250000,
        gain=5
    )

    # Manejo de cierre con Ctrl+C
    def sig_handler(sig, frame):
        rx_node.stop_rx()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)

    rx_node.start_rx()

    print("Escuchando... Presiona Ctrl+C para salir.")
    
    # Bucle principal para extraer mensajes de la cola de GNU Radio
    try:
        while True:
            # Revisamos si el bloque msg_debug recibió algo
            if rx_node.msg_debug.num_messages() > 0:
                # Extraemos el mensaje de la cola 'store'
                msg = rx_node.msg_debug.get_message(0)
                # Convertimos el mensaje (PDU) a un array de Python
                payload = list(gr.pdu.to_numpy(msg))
                save_to_file(payload)
                # Borramos el mensaje procesado para limpiar la cola
                rx_node.msg_debug.delete_message(0)
            
            time.sleep(0.1) # Pequeña pausa para no saturar la CPU
    except KeyboardInterrupt:
        rx_node.stop_rx()