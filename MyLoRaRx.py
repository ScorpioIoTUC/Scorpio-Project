#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import time
from datetime import datetime
from gnuradio import gr, blocks, soapy
import gnuradio.lora_sdr as lora_sdr
import pmt

class MyLoraRx(gr.top_block):
    def __init__(self, samp_rate=1000000, 
                 center_freq=915000000, 
                 bw=250000, 
                 sf=7, 
                 gain=40,
                 cr=1,
                 has_crc=True,
                 impl_head=False,
                 pay_len=64,
                 sync_word=0x12,
                 soft_decoding=True,
                 ldro_mode=2,
                 print_rx=[False,False]):
        
        gr.top_block.__init__(self, "My LoRa Receiver")
        
        # 1. Fuente RTL-SDR
        self.src = soapy.source('driver=rtlsdr', "fc32", 1, '', '', [''], [''])
        self.src.set_sample_rate(0, samp_rate)
        self.src.set_frequency(0, center_freq)
        self.src.set_gain_mode(0, False)
        self.src.set_gain(0, gain)

        # 2. Decodificador LoRa
        self.lora_rx = lora_sdr.lora_sdr_lora_rx(
            bw=bw, 
            cr=cr, 
            has_crc=has_crc, 
            impl_head=impl_head, 
            pay_len=pay_len,
            samp_rate=samp_rate, 
            sf=sf, 
            sync_word=[sync_word],
            soft_decoding=soft_decoding, 
            ldro_mode=ldro_mode, 
            print_rx=print_rx
        )

        # 3. Message Debug
        self.msg_debug = blocks.message_debug()

        # Conexiones
        self.connect((self.src, 0), (self.lora_rx, 0))
        self.msg_connect((self.lora_rx, 'out'), (self.msg_debug, 'store'))

    def start_rx(self):
        self.start()
        print(f"[*] Receptor activo: {self.src.get_frequency(0)/1e6} MHz")
        print("[*] Presiona Ctrl+C para salir de forma segura.")

    def stop_rx(self):
        """Detiene los hilos de GNU Radio de forma limpia."""
        self.stop()
        self.wait()
        print("\n[!] SDR y flujos detenidos correctamente.")

def procesar_dato(msg_pmt):
    """Extrae la data de forma segura manejando PDUs o Blobs directamente."""
    try:
        # Verificamos si es un par (PDU estándar)
        if pmt.is_pair(msg_pmt):
            data_part = pmt.cdr(msg_pmt)
        else:
            # Si no es un par, asumimos que el mensaje es el dato en sí (Blob/Vector)
            data_part = msg_pmt
        
        # Convertimos a formato Python
        payload = pmt.to_python(data_part)
        
        # Si es un string o bytes, lo limpiamos
        if isinstance(payload, (bytes, list)):
            mensaje = "".join(chr(b) for b in payload if 32 <= b <= 126)
        else:
            mensaje = str(payload)

        # Guardar con fecha y hora
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("lora_log.txt", "a") as f:
            f.write(f"[{timestamp}] {mensaje}\n")
        
        print(f"--- RECIBIDO: {mensaje}")

    except Exception as e:
        print(f"Error decodificando PMT: {e}")

if __name__ == '__main__':
    receptor = MyLoraRx(center_freq=915e6, sf=7, gain=5)

    def signal_handler(sig, frame):
        receptor.stop()
        receptor.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    receptor.start_rx()

    # Variables para control de la cola
    mensajes_procesados = 0

    try:
        # Bucle de escucha activo
        while True:
            total_actual = receptor.msg_debug.num_messages()
            
            if total_actual > mensajes_procesados:
                # Procesamos todos los nuevos mensajes que hayan llegado
                while mensajes_procesados < total_actual:
                    msg = receptor.msg_debug.get_message(mensajes_procesados)
                    procesar_dato(msg)
                    mensajes_procesados += 1
            
            time.sleep(0.2) # Latencia baja para respuesta rápida al teclado
            
    except KeyboardInterrupt:
        # Esto captura el Ctrl+C perfectamente
        print("\n[!] Interrupción detectada...")
    finally:
        # Pase lo que pase, cerramos la SDR para no bloquear el puerto USB
        receptor.stop_rx()
        sys.exit(0)